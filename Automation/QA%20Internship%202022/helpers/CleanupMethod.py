import os
import shutil
import time
from pathlib import Path

class CleanupMethod:
    
    def reportsCleanup(self):
        root = self.get_project_root()
        allureReportsPath = os.path.join(root, 'results')
        self.delete_dir_content(allureReportsPath)
        
    def get_project_root(self) -> Path:
        return Path(__file__).parent.parent
    
    def delete_dir_content(self, path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def cleanup_logs(self, path):
        try:
            with open(path, 'w') as g:
                g.truncate()
            g.close()
            os.remove(path)
        except WindowsError:
            time.sleep(5)
