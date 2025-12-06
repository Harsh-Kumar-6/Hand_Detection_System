\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{titlesec}
\usepackage{ulem}

\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}

\title{\textbf{Hand Distance Monitor using OpenCV}}
\author{}
\date{}

\begin{document}

\maketitle

\section{Overview}

This project implements a real-time \textbf{Hand Distance Monitor} using
OpenCV and NumPy. A virtual rectangular box is drawn on the screen, and the
distance of the detected hand from this box is computed. Depending on the
distance, the system classifies the state into:

\begin{itemize}
    \item \textbf{SAFE} (green)
    \item \textbf{WARNING} (yellow)
    \item \textbf{DANGER} (red)
\end{itemize}

Additional features include FPS calculation, debugging mask view, fullscreen
display, and adjustable distance thresholds using trackbars.

\section{Features}

\begin{itemize}
    \item Real-time hand detection using HSV-based skin segmentation.
    \item Adjustable SAFE and WARN distances through OpenCV trackbars.
    \item Virtual safety box with distance-based state classification.
    \item Side-by-side view of RGB frame and mask for debugging.
    \item Fullscreen UI with screenshot support.
    \item FPS counter.
\end{itemize}

\section{Requirements}

Install the dependencies using:

\begin{verbatim}
pip install -r requirements.txt
\end{verbatim}

\subsection*{requirements.txt}

\begin{verbatim}
opencv-python
numpy
\end{verbatim}

\section{How to Run}

Run the application with:

\begin{verbatim}
python main.py --cam 0
\end{verbatim}

\noindent
Use:

\begin{itemize}
    \item \verb!--cam 0! → laptop webcam
    \item \verb!--cam 1! → external USB camera
\end{itemize}

\section{Controls}

\begin{itemize}
    \item \textbf{ESC} – Quit program
    \item \textbf{S} – Save screenshot (demo\_screenshot.png)
\end{itemize}

Trackbars (in the ``Controls'' window):

\begin{itemize}
    \item \textbf{SAFE} – Outer threshold for safe distance
    \item \textbf{WARN} – Threshold for warning/danger zones
\end{itemize}

\section{How It Works}

\begin{enumerate}
    \item Capture frame from webcam.
    \item Convert frame to HSV color space.
    \item Apply two skin-color HSV ranges.
    \item Clean the mask using Gaussian blur and morphological operations.
    \item Find the largest contour (assumed to be the hand).
    \item Compute contour moments to find the hand's center.
    \item Compute distance to the virtual box.
    \item Display system state (SAFE/WARNING/DANGER).
\end{enumerate}

\section{Project Structure}

\begin{verbatim}
project/
│
├── main.py
├── requirements.txt
└── README.md (this file)
\end{verbatim}

\section{Notes}

\begin{itemize}
    \item Works best in environments with stable lighting.
    \item Skin-like backgrounds (yellow or beige walls) may reduce accuracy.
    \item For higher accuracy, consider using MediaPipe Hands instead of HSV.
\end{itemize}

\section{Future Improvements}

\begin{itemize}
    \item Replace HSV-based detection with MediaPipe Hands.
    \item Add depth estimation using stereo or monocular cues.
    \item Implement audio alerts for danger zone.
\end{itemize}

\end{document}
