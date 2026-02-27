/**
 * =============================================================================
 * GOOGLE DRIVE → GITHUB ACTIONS BRIDGE
 * =============================================================================
 * Watches a Google Drive folder for new files and triggers a GitHub Actions
 * workflow to download and process them.
 *
 * Setup:
 *   1. Open https://script.google.com → New Project
 *   2. Paste this code
 *   3. Set Script Properties (Project Settings → Script Properties):
 *      - GITHUB_TOKEN:    Fine-grained PAT with actions:write scope
 *      - GITHUB_REPO:     FehrAdvice-Partners-AG/complementarity-context-framework
 *      - GITHUB_BRANCH:   main
 *      - DRIVE_FOLDER_ID: Google Drive folder ID to watch
 *   4. Run setupTrigger() once to install the time-based trigger
 *   5. Done! New files auto-trigger GitHub Actions
 *
 * Architecture:
 *   Google Drive Folder
 *       ↓ (every 5 min check)
 *   Apps Script (this file)
 *       ↓ (workflow_dispatch POST)
 *   GitHub Actions → fetch-google-drive.yml
 *       ↓ (gdown + pdftotext + commit)
 *   Repository ← git pull
 *
 * Version: 1.0.0
 * Created: 2026-02-19
 * =============================================================================
 */

// =============================================================================
// CONFIGURATION (read from Script Properties)
// =============================================================================

function getConfig() {
  const props = PropertiesService.getScriptProperties();
  return {
    githubToken:   props.getProperty('GITHUB_TOKEN'),
    githubRepo:    props.getProperty('GITHUB_REPO') || 'FehrAdvice-Partners-AG/complementarity-context-framework',
    githubBranch:  props.getProperty('GITHUB_BRANCH') || 'main',
    driveFolderId: props.getProperty('DRIVE_FOLDER_ID'),
    workflow:      'fetch-google-drive.yml',
  };
}

// =============================================================================
// MAIN: Check folder for new files
// =============================================================================

/**
 * Checks the watched Drive folder for files added in the last 10 minutes.
 * Triggers GitHub Actions for each new file found.
 * Called by time-based trigger (every 5 minutes).
 */
function checkForNewFiles() {
  const config = getConfig();

  if (!config.githubToken || !config.driveFolderId) {
    console.error('Missing config. Set GITHUB_TOKEN and DRIVE_FOLDER_ID in Script Properties.');
    return;
  }

  const folder = DriveApp.getFolderById(config.driveFolderId);
  const files = folder.getFiles();
  const cutoff = new Date(Date.now() - 10 * 60 * 1000); // 10 minutes ago

  // Track processed files to avoid duplicates
  const processedKey = 'PROCESSED_FILES';
  const props = PropertiesService.getScriptProperties();
  const processed = JSON.parse(props.getProperty(processedKey) || '{}');

  let newCount = 0;

  while (files.hasNext()) {
    const file = files.next();
    const fileId = file.getId();
    const created = file.getDateCreated();
    const name = file.getName();

    // Skip already processed files
    if (processed[fileId]) {
      continue;
    }

    // Skip files older than cutoff (only process recent additions)
    // But also process never-seen files regardless of age (first run)
    if (created < cutoff && Object.keys(processed).length > 0) {
      continue;
    }

    console.log('New file detected: ' + name + ' (' + fileId + ')');

    // Determine if this is a PDF that should be split (journal volume)
    const isPdf = name.toLowerCase().endsWith('.pdf');
    const isJournal = /vol|volume|issue|journal|jep|aer|qje|ecma/i.test(name);
    const splitPapers = isPdf && isJournal;

    // Make file publicly accessible (Viewer)
    try {
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      console.log('  Set sharing: Anyone with link (Viewer)');
    } catch (e) {
      console.warn('  Could not set sharing: ' + e.message);
      // Continue anyway - file might already be shared
    }

    // Trigger GitHub Actions
    const success = triggerGitHubWorkflow(config, fileId, name, isPdf, splitPapers);

    if (success) {
      // Mark as processed
      processed[fileId] = {
        name: name,
        triggered: new Date().toISOString(),
        splitPapers: splitPapers,
      };
      newCount++;
      console.log('  Triggered GitHub Actions for: ' + name);
    } else {
      console.error('  FAILED to trigger for: ' + name);
    }
  }

  // Save processed state
  props.setProperty(processedKey, JSON.stringify(processed));

  if (newCount > 0) {
    console.log('Total new files processed: ' + newCount);
  }
}

// =============================================================================
// GITHUB API: Trigger workflow_dispatch
// =============================================================================

/**
 * Triggers the fetch-google-drive.yml workflow via GitHub API.
 */
function triggerGitHubWorkflow(config, fileId, fileName, convertPdf, splitPapers) {
  const url = 'https://api.github.com/repos/' + config.githubRepo +
              '/actions/workflows/' + config.workflow + '/dispatches';

  const payload = {
    ref: config.githubBranch,
    inputs: {
      file_id: fileId,
      output_name: fileName,
      convert_pdf: convertPdf ? 'true' : 'false',
      split_papers: splitPapers ? 'true' : 'false',
      target_branch: config.githubBranch,
    },
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'Authorization': 'token ' + config.githubToken,
      'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    const code = response.getResponseCode();

    if (code === 204) {
      return true;
    } else {
      console.error('GitHub API error ' + code + ': ' + response.getContentText());
      return false;
    }
  } catch (e) {
    console.error('Request failed: ' + e.message);
    return false;
  }
}

// =============================================================================
// SETUP: Install time-based trigger
// =============================================================================

/**
 * Run this ONCE to install the time-based trigger.
 * Checks every 5 minutes for new files.
 */
function setupTrigger() {
  // Remove existing triggers for this function
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    if (trigger.getHandlerFunction() === 'checkForNewFiles') {
      ScriptApp.deleteTrigger(trigger);
      console.log('Removed existing trigger');
    }
  });

  // Create new 5-minute trigger
  ScriptApp.newTrigger('checkForNewFiles')
    .timeDriven()
    .everyMinutes(5)
    .create();

  console.log('Trigger installed: checkForNewFiles every 5 minutes');

  // Validate config
  const config = getConfig();
  const missing = [];
  if (!config.githubToken) missing.push('GITHUB_TOKEN');
  if (!config.driveFolderId) missing.push('DRIVE_FOLDER_ID');

  if (missing.length > 0) {
    console.warn('WARNING: Missing Script Properties: ' + missing.join(', '));
    console.warn('Go to Project Settings → Script Properties to set them.');
  } else {
    console.log('Config OK. Watching folder: ' + config.driveFolderId);
    console.log('Triggering repo: ' + config.githubRepo + ' @ ' + config.githubBranch);
  }
}

// =============================================================================
// UTILITIES
// =============================================================================

/**
 * Manual trigger: Process a specific file by ID.
 * Useful for testing or re-processing.
 */
function processFileManually(fileId) {
  const config = getConfig();
  const file = DriveApp.getFileById(fileId);
  const name = file.getName();
  const isPdf = name.toLowerCase().endsWith('.pdf');
  const splitPapers = isPdf && /vol|volume|issue|journal/i.test(name);

  console.log('Manual trigger: ' + name);
  const success = triggerGitHubWorkflow(config, fileId, name, isPdf, splitPapers);
  console.log(success ? 'SUCCESS' : 'FAILED');
}

/**
 * List all files in the watched folder (for debugging).
 */
function listWatchedFolder() {
  const config = getConfig();
  const folder = DriveApp.getFolderById(config.driveFolderId);
  const files = folder.getFiles();

  console.log('Folder: ' + folder.getName());
  console.log('ID: ' + config.driveFolderId);
  console.log('---');

  let count = 0;
  while (files.hasNext()) {
    const file = files.next();
    console.log(file.getName() + ' | ' + file.getId() + ' | ' +
                file.getDateCreated().toISOString() + ' | ' +
                (file.getSize() / 1024 / 1024).toFixed(1) + ' MB');
    count++;
  }
  console.log('---');
  console.log('Total files: ' + count);
}

/**
 * Show processed files history.
 */
function showProcessedHistory() {
  const props = PropertiesService.getScriptProperties();
  const processed = JSON.parse(props.getProperty('PROCESSED_FILES') || '{}');
  const entries = Object.entries(processed);

  console.log('Processed files: ' + entries.length);
  entries.forEach(function([id, info]) {
    console.log('  ' + info.name + ' → ' + info.triggered +
                (info.splitPapers ? ' [SPLIT]' : ''));
  });
}

/**
 * Reset processed files tracker (re-process everything).
 */
function resetProcessedHistory() {
  const props = PropertiesService.getScriptProperties();
  props.deleteProperty('PROCESSED_FILES');
  console.log('Processed history cleared. Next run will process all recent files.');
}

// =============================================================================
// JEP ARCHIVE: Download ALL JEP PDFs directly from AEA website
// =============================================================================
// Key insight: EVERY JEP paper has a PDF at:
//   https://pubs.aeaweb.org/doi/pdfplus/{DOI}
// We do NOT need CrossRef PDF links. We just need DOIs from CrossRef,
// then construct the AEA URL directly.
// =============================================================================

var JEP_ISSN = '0895-3309';
var CROSSREF_BASE = 'https://api.crossref.org';
var AEA_PDF_BASE = 'https://pubs.aeaweb.org/doi/pdfplus/';
var BATCH_SIZE = 20;        // Papers per CrossRef page (metadata)
var PDF_LIMIT = 6;          // Max PDF downloads per run (AEA rate limit)
var DELAY_BETWEEN_MS = 3000; // 3 sec between downloads (be polite to AEA)
var MAX_RUNTIME_MS = 270000; // 4.5 min (Apps Script limit = 6 min)

/**
 * AUTO-TRIGGER: Downloads JEP PDFs in batches.
 * Called every 10 minutes by setupArchiveTrigger().
 * Saves progress in Script Properties so it can resume.
 */
function downloadJepArchiveAuto() {
  var props = PropertiesService.getScriptProperties();
  var config = getConfig();
  var folderId = props.getProperty('JEP_ARCHIVE_FOLDER_ID') || config.driveFolderId;

  if (!folderId) {
    console.error('No folder ID. Set JEP_ARCHIVE_FOLDER_ID or DRIVE_FOLDER_ID.');
    return;
  }

  var folder = DriveApp.getFolderById(folderId);
  var offset = parseInt(props.getProperty('JEP_ARCHIVE_OFFSET') || '0', 10);
  var totalSaved = parseInt(props.getProperty('JEP_ARCHIVE_SAVED') || '0', 10);
  var totalSkipped = parseInt(props.getProperty('JEP_ARCHIVE_SKIPPED') || '0', 10);
  var startTime = Date.now();

  console.log('=== JEP Archive Download ===');
  console.log('Offset: ' + offset + ' | Saved so far: ' + totalSaved + ' | Skipped: ' + totalSkipped);

  // Fetch batch from CrossRef
  var url = CROSSREF_BASE + '/journals/' + JEP_ISSN + '/works' +
            '?offset=' + offset +
            '&rows=' + BATCH_SIZE +
            '&sort=published&order=asc' +
            '&mailto=research@fehradvice.com';

  var resp;
  try {
    resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  } catch (e) {
    console.error('CrossRef fetch failed: ' + e.message);
    return;
  }

  if (resp.getResponseCode() !== 200) {
    console.error('CrossRef HTTP ' + resp.getResponseCode());
    return;
  }

  var data = JSON.parse(resp.getContentText());
  var items = data.message.items || [];
  var totalResults = data.message['total-results'] || 0;

  console.log('CrossRef: ' + items.length + ' items (total: ' + totalResults + ')');

  if (items.length === 0) {
    console.log('ARCHIVE COMPLETE! All ' + totalResults + ' papers processed.');
    console.log('Total saved: ' + totalSaved + ' | Skipped: ' + totalSkipped);
    // Remove trigger
    removeTrigger_('downloadJepArchiveAuto');
    return;
  }

  var batchSaved = 0;
  var batchSkipped = 0;
  var pdfDownloads = 0; // Track actual PDF downloads (not skips)

  for (var i = 0; i < items.length; i++) {
    // Check runtime limit
    if (Date.now() - startTime > MAX_RUNTIME_MS) {
      console.log('Runtime limit reached. Saving progress at offset ' + (offset + i));
      props.setProperty('JEP_ARCHIVE_OFFSET', String(offset + i));
      props.setProperty('JEP_ARCHIVE_SAVED', String(totalSaved + batchSaved));
      props.setProperty('JEP_ARCHIVE_SKIPPED', String(totalSkipped + batchSkipped));
      return;
    }

    // Stop after PDF_LIMIT actual downloads (AEA rate limit)
    if (pdfDownloads >= PDF_LIMIT) {
      console.log('PDF limit reached (' + PDF_LIMIT + ' downloads). Pausing until next run.');
      props.setProperty('JEP_ARCHIVE_OFFSET', String(offset + i));
      props.setProperty('JEP_ARCHIVE_SAVED', String(totalSaved + batchSaved));
      props.setProperty('JEP_ARCHIVE_SKIPPED', String(totalSkipped + batchSkipped));
      return;
    }

    var item = items[i];
    var doi = item.DOI || '';
    var titleArr = item.title || ['Untitled'];
    var title = titleArr[0];
    var authors = item.author || [];
    var volume = item.volume || '?';
    var issue = item.issue || '?';
    var year = '?';
    var published = item['published-print'] || item['published-online'] || {};
    var dateParts = (published['date-parts'] || [[]])[0];
    if (dateParts.length > 0) year = dateParts[0];

    var firstAuthor = 'unknown';
    if (authors.length > 0) {
      firstAuthor = authors[0].family || authors[0].name || 'unknown';
    }

    // Construct filename
    var safeAuthor = firstAuthor.replace(/[^a-zA-Z0-9]/g, '');
    var safeTitle = title.substring(0, 50).replace(/[^a-zA-Z0-9 ]/g, '').replace(/ +/g, '_');
    var fileName = 'JEP_' + year + '_V' + volume + '_I' + issue + '_' + safeAuthor + '_' + safeTitle + '.pdf';

    // Check if already downloaded (by DOI in file description)
    var existing = folder.searchFiles('title contains "JEP_' + year + '_V' + volume + '_I' + issue + '_' + safeAuthor + '"');
    if (existing.hasNext()) {
      console.log('  SKIP (exists): ' + fileName.substring(0, 70));
      batchSkipped++;
      continue;
    }

    if (!doi) {
      console.log('  SKIP (no DOI): ' + title.substring(0, 60));
      batchSkipped++;
      continue;
    }

    // KEY FIX: Construct PDF URL directly from DOI
    // Every JEP paper is available at: https://pubs.aeaweb.org/doi/pdfplus/{DOI}
    var pdfUrl = AEA_PDF_BASE + doi;

    try {
      var pdfResp = UrlFetchApp.fetch(pdfUrl, {
        muteHttpExceptions: true,
        followRedirects: true,
      });

      var pdfCode = pdfResp.getResponseCode();
      var contentType = pdfResp.getHeaders()['Content-Type'] || '';

      if (pdfCode === 200 && contentType.indexOf('pdf') !== -1) {
        var blob = pdfResp.getBlob().setName(fileName);
        var file = folder.createFile(blob);
        file.setDescription('DOI: ' + doi + '\nTitle: ' + title + '\nAuthors: ' +
                           authors.map(function(a) { return (a.given || '') + ' ' + (a.family || a.name || ''); }).join(', '));
        var sizeKB = (blob.getBytes().length / 1024).toFixed(0);
        console.log('  ✅ ' + pdfDownloads + '/' + PDF_LIMIT + ': ' + fileName.substring(0, 60) + ' (' + sizeKB + ' KB)');
        batchSaved++;
        pdfDownloads++;

        // Longer pause between actual PDF downloads (AEA rate limit)
        if (pdfDownloads < PDF_LIMIT) {
          Utilities.sleep(DELAY_BETWEEN_MS);
        }
      } else if (pdfCode === 403 || pdfCode === 429) {
        // Rate limited - stop immediately and retry next run
        console.log('  ⚠️ RATE LIMITED (HTTP ' + pdfCode + '). Stopping. Will retry in 10 min.');
        props.setProperty('JEP_ARCHIVE_OFFSET', String(offset + i));
        props.setProperty('JEP_ARCHIVE_SAVED', String(totalSaved + batchSaved));
        props.setProperty('JEP_ARCHIVE_SKIPPED', String(totalSkipped + batchSkipped));
        return;
      } else {
        console.log('  ❌ KEIN PDF (HTTP ' + pdfCode + '): ' + doi);
        batchSkipped++;
      }
    } catch (e) {
      console.log('  ❌ FEHLER: ' + doi + ' → ' + e.message);
      batchSkipped++;
    }

    // Small delay between CrossRef metadata processing
    Utilities.sleep(300);
  }

  // Update progress
  var newOffset = offset + items.length;
  props.setProperty('JEP_ARCHIVE_OFFSET', String(newOffset));
  props.setProperty('JEP_ARCHIVE_SAVED', String(totalSaved + batchSaved));
  props.setProperty('JEP_ARCHIVE_SKIPPED', String(totalSkipped + batchSkipped));

  var pct = ((newOffset / totalResults) * 100).toFixed(1);
  console.log('--- Batch done ---');
  console.log('Saved: ' + batchSaved + ' | Skipped: ' + batchSkipped);
  console.log('Progress: ' + newOffset + '/' + totalResults + ' (' + pct + '%)');
  console.log('Total saved: ' + (totalSaved + batchSaved));
}

/**
 * Setup: Install 10-minute trigger for archive download.
 */
function setupArchiveTrigger() {
  removeTrigger_('downloadJepArchiveAuto');
  ScriptApp.newTrigger('downloadJepArchiveAuto')
    .timeDriven()
    .everyMinutes(10)
    .create();
  console.log('Archiv-Trigger: alle 10 min bis komplett');
}

/**
 * Reset: Start archive download from beginning.
 */
function resetArchiveProgress() {
  var props = PropertiesService.getScriptProperties();
  props.deleteProperty('JEP_ARCHIVE_OFFSET');
  props.deleteProperty('JEP_ARCHIVE_SAVED');
  props.deleteProperty('JEP_ARCHIVE_SKIPPED');
  console.log('Archive progress reset. Next run starts from offset 0.');
}

/**
 * Show archive download status.
 */
function showArchiveStatus() {
  var props = PropertiesService.getScriptProperties();
  var offset = props.getProperty('JEP_ARCHIVE_OFFSET') || '0';
  var saved = props.getProperty('JEP_ARCHIVE_SAVED') || '0';
  var skipped = props.getProperty('JEP_ARCHIVE_SKIPPED') || '0';
  console.log('=== JEP Archive Status ===');
  console.log('Offset (next batch starts here): ' + offset);
  console.log('Total saved: ' + saved);
  console.log('Total skipped: ' + skipped);
  console.log('Total processed: ' + (parseInt(saved) + parseInt(skipped)));
}

/**
 * Helper: Remove all triggers for a given function.
 */
function removeTrigger_(functionName) {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === functionName) {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }
}

// =============================================================================
// UTILITIES
// =============================================================================

/**
 * Test the GitHub connection (without downloading anything).
 */
function testGitHubConnection() {
  const config = getConfig();

  if (!config.githubToken) {
    console.error('GITHUB_TOKEN not set in Script Properties');
    return;
  }

  const url = 'https://api.github.com/repos/' + config.githubRepo;
  const options = {
    method: 'get',
    headers: {
      'Authorization': 'token ' + config.githubToken,
      'Accept': 'application/vnd.github+json',
    },
    muteHttpExceptions: true,
  };

  const response = UrlFetchApp.fetch(url, options);
  const code = response.getResponseCode();

  if (code === 200) {
    const repo = JSON.parse(response.getContentText());
    console.log('Connection OK!');
    console.log('  Repo: ' + repo.full_name);
    console.log('  Default branch: ' + repo.default_branch);
    console.log('  Private: ' + repo.private);
  } else {
    console.error('Connection FAILED (HTTP ' + code + ')');
    console.error(response.getContentText());
  }
}
