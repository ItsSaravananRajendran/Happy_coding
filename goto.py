import sublime, sublime_plugin

class DupCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print (self.view.size())
        regions = [ sublime.Region(0, self.view.size()) ]
        regions = self.view.split_by_newlines(regions[0])
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                line_contents = self.view.substr(line) + '\n'
                self.view.insert(edit, line.begin(), line_contents)
            else:
                self.view.insert(edit, region.begin(), self.view.substr(region))
