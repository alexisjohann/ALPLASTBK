% =============================================================================
% FEHRADVICE REPORT DOCUMENT CLASS
% =============================================================================
% Based on: Corporate-Identity-Guide-FAP-EN-231007 2.pdf
% Version: 1.0 (January 2026)
%
% Usage:
%   \documentclass{fehradvice-report}
%
% Requires: XeLaTeX or LuaLaTeX for proper font rendering
% =============================================================================

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fehradvice-report}[2026/01/26 FehrAdvice Report Class]

% =============================================================================
% BASE CLASS
% =============================================================================

\LoadClass[11pt,a4paper]{article}

% =============================================================================
% REQUIRED PACKAGES
% =============================================================================

\RequirePackage[
    top=25mm,
    bottom=20mm,
    left=25mm,
    right=20mm
]{geometry}

\RequirePackage{fehradvice-colors}
\RequirePackage{fehradvice-fonts}

\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{longtable}
\RequirePackage{multirow}
\RequirePackage{array}
\RequirePackage{colortbl}
\RequirePackage{float}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{hyperref}
\RequirePackage{tcolorbox}
\RequirePackage{enumitem}
\RequirePackage{csquotes}

% =============================================================================
% HYPERREF SETUP
% =============================================================================

\hypersetup{
    colorlinks=true,
    linkcolor=fadarkblue,
    citecolor=fadarkblue,
    urlcolor=fadarkblue,
    filecolor=fadarkblue
}

% =============================================================================
% PAGE HEADER & FOOTER
% =============================================================================

\pagestyle{fancy}
\fancyhf{}

% Header
\fancyhead[L]{\small\color{fadarkgray}\@title}
\fancyhead[R]{\small\color{fadarkgray}\@date}

% Footer
\fancyfoot[L]{\small\color{fadarkblue}FehrAdvice \& Partners AG}
\fancyfoot[R]{\small\color{fadarkgray}Seite \thepage\ von \pageref{LastPage}}

% Header/Footer line
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0pt}

% First page style (no header)
\fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[L]{\small\color{fadarkblue}FehrAdvice \& Partners AG}
    \fancyfoot[R]{\small\color{fadarkgray}Seite \thepage\ von \pageref{LastPage}}
    \renewcommand{\headrulewidth}{0pt}
}

% =============================================================================
% TITLE PAGE
% =============================================================================

\renewcommand{\maketitle}{
    \begin{titlepage}
        \begin{center}
            \vspace*{2cm}

            % Logo placeholder
            \includegraphics[width=5cm]{fehradvice-logo}

            \vspace{2cm}

            % Title
            {\sffamily\bfseries\Huge\color{fadarkblue}\@title\par}

            \vspace{1cm}

            % Subtitle (if defined)
            \ifdefined\@subtitle
                {\sffamily\Large\color{falightblue}\@subtitle\par}
                \vspace{1cm}
            \fi

            % Horizontal line
            {\color{fadarkblue}\rule{\textwidth}{2pt}}

            \vspace{2cm}

            % Author
            {\large\@author\par}

            \vspace{0.5cm}

            % Date
            {\large\@date\par}

            \vfill

            % Footer info
            {\small\color{fadarkgray}
            FehrAdvice \& Partners AG\\
            Behavioral Economics Consultancy Group
            }
        \end{center}
    \end{titlepage}
    \thispagestyle{plain}
}

% Subtitle command
\newcommand{\subtitle}[1]{\def\@subtitle{#1}}

% =============================================================================
% TABLE STYLING
% =============================================================================

% FehrAdvice table style
\newenvironment{fatable}[1][]{%
    \rowcolors{2}{fawhite}{falightgray}
    \begin{tabular}{#1}
    \rowcolor{fadarkblue}
}{%
    \end{tabular}
}

% Table header style
\newcommand{\fahead}[1]{\textcolor{fawhite}{\bfseries #1}}

% =============================================================================
% BOX STYLES
% =============================================================================

% Info box (blue)
\newtcolorbox{fainfobox}[1][]{
    colback=falightgray,
    colframe=fadarkblue,
    coltitle=fawhite,
    fonttitle=\sffamily\bfseries,
    title=#1
}

% Warning box (orange)
\newtcolorbox{fawarningbox}[1][Hinweis]{
    colback=faorange!10,
    colframe=faorange,
    coltitle=fawhite,
    fonttitle=\sffamily\bfseries,
    title=#1
}

% Success box (mint)
\newtcolorbox{fasuccessbox}[1][]{
    colback=famint!10,
    colframe=famint,
    coltitle=fawhite,
    fonttitle=\sffamily\bfseries,
    title=#1
}

% Quote box (accent font)
\newtcolorbox{faquotebox}{
    colback=falightgray,
    colframe=fadarkblue,
    leftrule=4pt,
    rightrule=0pt,
    toprule=0pt,
    bottomrule=0pt,
    fontupper=\accentfont\itshape\color{fadarkblue}
}

% =============================================================================
% LIST STYLING
% =============================================================================

\setlist[itemize]{
    label=\textcolor{fadarkblue}{\textbullet},
    leftmargin=*,
    itemsep=6pt
}

\setlist[enumerate]{
    label=\textcolor{fadarkblue}{\arabic*.},
    leftmargin=*,
    itemsep=6pt
}

% =============================================================================
% QUOTE STYLING
% =============================================================================

\renewenvironment{quote}{%
    \begin{faquotebox}
    «
}{%
    »
    \end{faquotebox}
}

% =============================================================================
% SWISS GERMAN SETTINGS
% =============================================================================

% Use « » for quotes
\renewcommand{\textquote}[1]{«#1»}

% Swiss number format: 1'000.00
\RequirePackage{siunitx}
\sisetup{
    group-separator = {'},
    group-minimum-digits = 4,
    output-decimal-marker = {.}
}

% =============================================================================
% DOCUMENT METADATA
% =============================================================================

\newcommand{\client}[1]{\def\@client{#1}}
\newcommand{\project}[1]{\def\@project{#1}}
\newcommand{\version}[1]{\def\@version{#1}}
\newcommand{\classification}[1]{\def\@classification{#1}}

% =============================================================================
% END OF CLASS
% =============================================================================

\endinput
