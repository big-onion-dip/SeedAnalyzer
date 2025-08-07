from gui import SeedAnalyzerApp

if __name__ == "__main__":
    app = SeedAnalyzerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
