// =============================================================================
// RESEARCHER PAPER SCRAPER — Core Logic (Researcher.gs)
// =============================================================================
//
// ZWEI WEGE, Forscher zu konfigurieren:
//
// 1. EMPFOHLEN: JSON-Config im Git-Repo (data/researcher-scraper-config.json)
//    → Wird automatisch via raw.githubusercontent.com geladen
//    → Neue Forscher hinzufuegen = JSON editieren + commit — fertig!
//    → Kein Zugriff auf Google Apps Script noetig
//
// 2. FALLBACK: Lokale RESEARCHER_* Globals (Researcher_Fehr.gs, etc.)
//    → Wird nur verwendet wenn GitHub-Fetch fehlschlaegt
//    → Weiterhin funktionsfaehig fuer Offline-Betrieb
//
// =============================================================================

var RES_GITHUB_OWNER = 'FehrAdvice-Partners-AG';
var RES_GITHUB_REPO  = 'complementarity-context-framework';

// Config-URL: raw.githubusercontent.com liefert die JSON direkt
var RES_CONFIG_URL = 'https://raw.githubusercontent.com/'
  + RES_GITHUB_OWNER + '/' + RES_GITHUB_REPO
  + '/main/data/researcher-scraper-config.json';

// =============================================================================
// CONFIG LADEN (GitHub → Fallback auf lokale Globals)
// =============================================================================

/**
 * Laedt Forscher-Config von GitHub (data/researcher-scraper-config.json).
 * Fallback: Lokale RESEARCHER_* Globals (alte Methode).
 *
 * @return {Array} Array von {name, url, folder} Objekten
 */
function loadResearcherConfig_() {
  // Versuch 1: Von GitHub laden
  try {
    var response = UrlFetchApp.fetch(RES_CONFIG_URL, {
      muteHttpExceptions: true,
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'EBF-ResearcherScraper/2.0'
      }
    });

    if (response.getResponseCode() === 200) {
      var json = JSON.parse(response.getContentText());
      if (json.researchers && json.researchers.length > 0) {
        Logger.log('Config geladen von GitHub: ' + json.researchers.length + ' Forscher');
        Logger.log('Config-Version: ' + (json._version || 'unbekannt'));
        return json.researchers;
      }
    } else {
      Logger.log('GitHub Config HTTP ' + response.getResponseCode() + ' — nutze Fallback');
    }
  } catch (e) {
    Logger.log('GitHub Config Fehler: ' + e.message + ' — nutze Fallback');
  }

  // Versuch 2: Fallback auf lokale RESEARCHER_* Globals
  Logger.log('Fallback: Suche lokale RESEARCHER_* Variablen...');
  var researchers = [];
  var globals = Object.keys(this);
  for (var i = 0; i < globals.length; i++) {
    if (globals[i].indexOf('RESEARCHER_') === 0) {
      var cfg = this[globals[i]];
      if (cfg && cfg.name && cfg.url && cfg.folder) {
        researchers.push(cfg);
      }
    }
  }

  if (researchers.length > 0) {
    Logger.log('Fallback: ' + researchers.length + ' Forscher aus lokalen Globals');
  } else {
    Logger.log('FEHLER: Weder GitHub-Config noch lokale Globals gefunden!');
  }

  return researchers;
}

// =============================================================================
// HAUPTFUNKTIONEN
// =============================================================================

/**
 * Laedt Config (von GitHub oder lokal) und scrapt alle Forscher-Webseiten.
 * Neue Forscher hinzufuegen: data/researcher-scraper-config.json editieren.
 */
function scrapeAllResearchers() {
  var folderId = PropertiesService.getScriptProperties().getProperty('DRIVE_FOLDER_ID');
  if (!folderId) {
    Logger.log('FEHLER: DRIVE_FOLDER_ID nicht gesetzt!');
    Logger.log('Gehe zu: Projekteinstellungen → Skripteigenschaften → DRIVE_FOLDER_ID');
    return;
  }

  var researchers = loadResearcherConfig_();

  Logger.log('');
  Logger.log('========================================');
  Logger.log('RESEARCHER SCRAPER — ' + researchers.length + ' Forscher');
  Logger.log('========================================');

  if (researchers.length === 0) {
    Logger.log('Keine Forscher konfiguriert!');
    return;
  }

  var successCount = 0;
  var errorCount = 0;

  for (var i = 0; i < researchers.length; i++) {
    try {
      scrapeResearcherSite_(researchers[i], folderId);
      successCount++;
      Utilities.sleep(5000);
    } catch (e) {
      Logger.log('FEHLER bei ' + researchers[i].name + ': ' + e.message);
      errorCount++;
    }
  }

  Logger.log('');
  Logger.log('========================================');
  Logger.log('ZUSAMMENFASSUNG: ' + successCount + ' OK, ' + errorCount + ' Fehler');
  Logger.log('========================================');
}

/**
 * Zeigt die aktuelle Config an (von GitHub oder Fallback).
 * Nuetzlich zum Debuggen und Pruefen ob neue Forscher erkannt werden.
 */
function showResearcherConfig() {
  var researchers = loadResearcherConfig_();
  Logger.log('');
  Logger.log('AKTUELLE RESEARCHER CONFIG:');
  Logger.log('');
  for (var i = 0; i < researchers.length; i++) {
    var r = researchers[i];
    Logger.log('  ' + (i + 1) + '. ' + r.name);
    Logger.log('     URL:    ' + r.url);
    Logger.log('     Folder: ' + r.folder);
    if (r.registry_id) {
      Logger.log('     ID:     ' + r.registry_id);
    }
    Logger.log('');
  }
}

function scrapeResearcherSite_(researcher, rootFolderId) {
  Logger.log('');
  Logger.log('=== ' + researcher.name + ' ===');
  Logger.log('URL: ' + researcher.url);

  var response = UrlFetchApp.fetch(researcher.url, {
    muteHttpExceptions: true,
    followRedirects: true,
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; ResearchScraper/1.0)'
    }
  });

  if (response.getResponseCode() !== 200) {
    Logger.log('HTTP ' + response.getResponseCode());
    return;
  }

  var html = response.getContentText();
  var pdfLinks = extractPdfLinksRes_(html, researcher.url);
  Logger.log('Gefunden: ' + pdfLinks.length + ' PDF-Links');

  if (pdfLinks.length === 0) return;

  // Drive-Ordner
  var researchersFolder = getOrCreateFolderRes_(rootFolderId, 'Researchers');
  var resFolder = getOrCreateFolderRes_(researchersFolder.getId(), researcher.folder);

  // Bereits vorhandene
  var existing = {};
  var files = resFolder.getFiles();
  while (files.hasNext()) {
    existing[files.next().getName()] = true;
  }

  // Neue PDFs laden
  var count = 0;
  var skipped = 0;

  for (var i = 0; i < pdfLinks.length; i++) {
    var link = pdfLinks[i];

    if (existing[link.filename]) {
      skipped++;
      continue;
    }

    try {
      Logger.log('  Lade: ' + link.url);
      var pdf = UrlFetchApp.fetch(link.url, {
        muteHttpExceptions: true,
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; ResearchScraper/1.0)'
        }
      });

      if (pdf.getResponseCode() === 200) {
        var blob = pdf.getBlob().setName(link.filename);
        var kb = Math.round(blob.getBytes().length / 1024);

        if (kb < 10) {
          Logger.log('  SKIP (zu klein, ' + kb + ' KB): ' + link.filename);
          continue;
        }

        var driveFile = resFolder.createFile(blob);
        Logger.log('  OK: ' + link.filename + ' (' + kb + ' KB)');

        triggerGitHubRes_(driveFile.getId(), link.filename);
        count++;
        Utilities.sleep(3000);
      } else {
        Logger.log('  HTTP ' + pdf.getResponseCode() + ': ' + link.url);
      }
    } catch (e) {
      Logger.log('  FEHLER: ' + link.filename + ' — ' + e.message);
    }
  }

  Logger.log('');
  Logger.log('ERGEBNIS ' + researcher.name + ':');
  Logger.log('  Neu heruntergeladen: ' + count);
  Logger.log('  Bereits vorhanden:   ' + skipped);
  Logger.log('  Total auf Webseite:  ' + pdfLinks.length);
}

// =============================================================================
// HILFSFUNKTIONEN
// =============================================================================

function extractPdfLinksRes_(html, baseUrl) {
  var links = [];
  var seen = {};

  // Origin aus URL extrahieren (z.B. https://www.econ.uzh.ch)
  var originMatch = baseUrl.match(/^(https?:\/\/[^\/]+)/);
  var origin = originMatch ? originMatch[1] : baseUrl.replace(/\/+$/, '');

  var pattern = /href\s*=\s*["']([^"']*\.pdf[^"']*?)["']/gi;
  var match;

  while ((match = pattern.exec(html)) !== null) {
    var href = match[1];

    // ./ am Anfang entfernen
    href = href.replace(/^\.\//, '');

    // URL aufloesen
    var url;
    if (href.match(/^https?:\/\//)) {
      url = href;
    } else if (href.charAt(0) === '/') {
      url = origin + href;
    } else {
      url = origin + '/' + href;
    }

    if (seen[url]) continue;
    seen[url] = true;

    // Dateiname
    var parts = url.split('/');
    var fname = decodeURIComponent(parts[parts.length - 1].split('?')[0]);
    if (!fname.match(/\.pdf$/i)) fname = fname + '.pdf';

    links.push({ url: url, filename: fname });
  }

  return links;
}

function getOrCreateFolderRes_(parentId, name) {
  var parent = DriveApp.getFolderById(parentId);
  var folders = parent.getFoldersByName(name);
  if (folders.hasNext()) return folders.next();
  return parent.createFolder(name);
}

function triggerGitHubRes_(fileId, filename) {
  var token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) {
    Logger.log('  WARN: Kein GITHUB_TOKEN — GitHub uebersprungen');
    return;
  }

  var payload = {
    ref: 'main',
    inputs: {
      file_id: fileId,
      output_name: filename,
      convert_pdf: 'true',
      split_papers: 'false'
    }
  };

  var options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'Authorization': 'token ' + token,
      'Accept': 'application/vnd.github.v3+json'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  var apiUrl = 'https://api.github.com/repos/'
    + RES_GITHUB_OWNER + '/' + RES_GITHUB_REPO
    + '/actions/workflows/fetch-google-drive.yml/dispatches';

  var resp = UrlFetchApp.fetch(apiUrl, options);
  Logger.log('  GitHub: HTTP ' + resp.getResponseCode());
}

// =============================================================================
// TRIGGER
// =============================================================================

function setupResearcherTrigger() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'scrapeAllResearchers') {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }

  var builder = ScriptApp.newTrigger('scrapeAllResearchers');
  var clock = builder.timeBased();
  clock.onWeekDay(ScriptApp.WeekDay.MONDAY);
  clock.atHour(6);
  clock.create();

  Logger.log('Trigger: scrapeAllResearchers Mo 06:00');
}
