"""
Visual Feedback Display System

This module provides a simple visual feedback display system for the contextual
intelligence features. It creates a basic GUI that can show visual feedback
without interfering with the DAW workflow.

Key Features:
- On-demand visual feedback display
- Non-intrusive overlay system
- Educational content display
- Musical element highlighting
- Suggestion indicators
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Optional
import threading
import time

from contextual_intelligence import VisualFeedback, VisualFeedbackType, MusicalElement


class VisualFeedbackDisplay:
    """Simple visual feedback display using tkinter."""
    
    def __init__(self):
        """Initialize the visual feedback display."""
        self.root: Optional[tk.Tk] = None
        self.feedback_text: Optional[scrolledtext.ScrolledText] = None
        self.status_label: Optional[ttk.Label] = None
        self.feedback_queue: List[VisualFeedback] = []
        self.is_running = False
        self.display_thread: Optional[threading.Thread] = None
        
    def start_display(self) -> None:
        """Start the visual feedback display in a separate thread."""
        if self.is_running:
            return
            
        self.is_running = True
        self.display_thread = threading.Thread(target=self._run_display, daemon=True)
        self.display_thread.start()
    
    def stop_display(self) -> None:
        """Stop the visual feedback display."""
        self.is_running = False
        if self.root:
            self.root.quit()
    
    def _run_display(self) -> None:
        """Run the display in the main thread."""
        self.root = tk.Tk()
        self.root.title("YesAnd Music - Visual Feedback")
        self.root.geometry("600x400")
        self.root.configure(bg='#2b2b2b')
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="Contextual Intelligence Feedback",
            font=('Arial', 14, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Feedback text area
        self.feedback_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff',
            selectbackground='#404040',
            font=('Consolas', 10)
        )
        self.feedback_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready for analysis",
            font=('Arial', 10)
        )
        self.status_label.grid(row=2, column=0, pady=(0, 5))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        clear_button = ttk.Button(
            button_frame,
            text="Clear Feedback",
            command=self.clear_display
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        close_button = ttk.Button(
            button_frame,
            text="Close",
            command=self.stop_display
        )
        close_button.pack(side=tk.LEFT)
        
        # Start the update loop
        self._update_display()
        
        # Run the GUI
        self.root.mainloop()
    
    def add_feedback(self, feedback: VisualFeedback) -> None:
        """Add visual feedback to the display queue.
        
        Args:
            feedback: The visual feedback to display
        """
        self.feedback_queue.append(feedback)
    
    def add_feedback_list(self, feedback_list: List[VisualFeedback]) -> None:
        """Add multiple visual feedback items to the display queue.
        
        Args:
            feedback_list: List of visual feedback items
        """
        self.feedback_queue.extend(feedback_list)
    
    def _update_display(self) -> None:
        """Update the display with new feedback."""
        if not self.is_running or not self.root:
            return
        
        # Process any new feedback
        if self.feedback_queue:
            for feedback in self.feedback_queue:
                self._display_feedback(feedback)
            self.feedback_queue.clear()
        
        # Schedule next update
        self.root.after(100, self._update_display)
    
    def _display_feedback(self, feedback: VisualFeedback) -> None:
        """Display a single feedback item.
        
        Args:
            feedback: The visual feedback to display
        """
        if not self.feedback_text:
            return
        
        # Get color based on element type
        color_map = {
            MusicalElement.BASS: "#4A90E2",      # Blue
            MusicalElement.MELODY: "#7ED321",    # Green
            MusicalElement.HARMONY: "#9013FE",   # Purple
            MusicalElement.RHYTHM: "#F5A623",    # Orange
            MusicalElement.DRUMS: "#D0021B",     # Red
        }
        
        color = color_map.get(feedback.element, "#FFFFFF")
        
        # Format the feedback message
        timestamp = time.strftime("%H:%M:%S", time.localtime(feedback.timestamp))
        message = f"[{timestamp}] {feedback.element.value.upper()}: {feedback.message}\n"
        
        # Insert with color
        self.feedback_text.insert(tk.END, message)
        
        # Apply color to the last line
        start_line = self.feedback_text.index("end-2l")
        end_line = self.feedback_text.index("end-1l")
        self.feedback_text.tag_add(f"color_{feedback.element.value}", start_line, end_line)
        self.feedback_text.tag_config(f"color_{feedback.element.value}", foreground=color)
        
        # Add additional data if available
        if feedback.data:
            data_text = f"    Data: {feedback.data}\n"
            self.feedback_text.insert(tk.END, data_text)
            self.feedback_text.tag_add(f"data_{feedback.element.value}", "end-2l", "end-1l")
            self.feedback_text.tag_config(f"data_{feedback.element.value}", foreground="#888888")
        
        # Scroll to bottom
        self.feedback_text.see(tk.END)
        
        # Update status
        if self.status_label:
            self.status_label.config(text=f"Last update: {timestamp}")
    
    def clear_display(self) -> None:
        """Clear the feedback display."""
        if self.feedback_text:
            self.feedback_text.delete(1.0, tk.END)
        if self.status_label:
            self.status_label.config(text="Display cleared")
    
    def show_help(self) -> None:
        """Show help information in the display."""
        help_text = """
YesAnd Music - Contextual Intelligence Help

Available Commands:
- load [FILE]                - Load MIDI project for analysis
- analyze bass               - Show bass line analysis and highlighting
- analyze melody             - Show melody analysis and highlighting
- analyze harmony            - Show harmony analysis and highlighting
- analyze rhythm             - Show rhythm analysis and highlighting
- analyze all                - Complete musical analysis
- get suggestions            - Get improvement suggestions
- apply suggestion [ID]      - Apply a specific suggestion
- show feedback              - Show visual feedback summary
- clear feedback             - Clear all visual feedback

Color Coding:
- Blue: Bass line elements
- Green: Melody elements
- Purple: Harmony elements
- Orange: Rhythm elements
- Red: Drum elements

The visual feedback provides:
- Musical element highlighting
- Analysis explanations
- Improvement suggestions
- Educational content
- Real-time updates

This display works alongside your DAW without interfering with your workflow.
        """
        
        if self.feedback_text:
            self.feedback_text.delete(1.0, tk.END)
            self.feedback_text.insert(1.0, help_text)
            self.feedback_text.tag_add("help", 1.0, tk.END)
            self.feedback_text.tag_config("help", foreground="#7ED321")
    
    def is_display_running(self) -> bool:
        """Check if the display is currently running."""
        return self.is_running and self.root is not None


# Global display instance
_display_instance: Optional[VisualFeedbackDisplay] = None


def get_display() -> VisualFeedbackDisplay:
    """Get the global visual feedback display instance.
    
    Returns:
        The global VisualFeedbackDisplay instance
    """
    global _display_instance
    if _display_instance is None:
        _display_instance = VisualFeedbackDisplay()
    return _display_instance


def start_visual_feedback() -> None:
    """Start the visual feedback display."""
    display = get_display()
    if not display.is_display_running():
        display.start_display()


def stop_visual_feedback() -> None:
    """Stop the visual feedback display."""
    display = get_display()
    if display.is_display_running():
        display.stop_display()


def add_visual_feedback(feedback: VisualFeedback) -> None:
    """Add visual feedback to the display.
    
    Args:
        feedback: The visual feedback to display
    """
    display = get_display()
    display.add_feedback(feedback)


def add_visual_feedback_list(feedback_list: List[VisualFeedback]) -> None:
    """Add multiple visual feedback items to the display.
    
    Args:
        feedback_list: List of visual feedback items
    """
    display = get_display()
    display.add_feedback_list(feedback_list)
