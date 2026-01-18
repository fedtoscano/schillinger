\version "2.25.12" 
\include "lilypond-book-preamble.ly"
    
color = #(define-music-function (parser location color) (string?) #{
        \once \override NoteHead.color = #(x11-color color)
        \once \override Stem.color = #(x11-color color)
        \once \override Rest.color = #(x11-color color)
        \once \override Beam.color = #(x11-color color)
     #})
    
\header { } 
\score  { 
 \new Voice { \new Voice { \time 4/4
                c' 2.  
                c' 4  
                c' 2  
                c' 4  
                c' 4  
                c' 4  
                c' 4  
                c' 2  
                c' 4  
                c' 2.  
                 } 
               
 
           } 
         
 
  } 
 
\paper { }
\layout {
  \context {
    \RemoveEmptyStaves
    \override VerticalAxisGroup.remove-first = ##t
  }
 }
 
