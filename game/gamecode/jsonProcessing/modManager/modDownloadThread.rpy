rpy python 3

init python:
    import os
    import requests
    import threading
    import ssl
    import shutil

    class DownloadThread(threading.Thread):
        def __init__(self, url):
            global warning
            super(DownloadThread, self).__init__()
            self.daemon = True
            self._stop_event = threading.Event()
            self.fp = open(os.path.join(mod_folder, "mod.zip"), 'w+b')
            self.url = requests.Session().get(url, stream=True, headers ={'User-Agent': 'Mozilla/5.0'})
            if 'Content-Length' in self.url.headers:
                self.totalSize = int(self.url.headers["Content-Length"])
            else:
                self.totalSize = 0
            self.chunkSize = 8192
            self.chunkCount = 0

        def stop(self):
            global dlStatus, dlPercentageStatusText, dlPercentageText, dlPercentage, thread, warning
            self._stop_event.set()
            try:
                self.fp.flush()
                self.fp.close()
            except Exception as e:
                print(e)
            if os.path.exists(os.path.join(mod_folder, "mod.zip")):
                try:
                    validateAndRenameZip(os.path.join(mod_folder, "mod.zip")) # rename zip for later install
                except Exception as e:
                    print(e)

            dlStatus = "Waiting"
            dlPercentage = 0
            dlPercentageText = 0
            dlPercentageStatusText = "0B / 0B"
            warning = ""

            thread = ""
            renpy.notify("Download finished!")

            updateModMetadata()

            renpy.restart_interaction()

        def stopped(self):
            return self._stop_event.is_set()

        def run(self):

            renpy.notify("Download started... (expect lag!)")

            global dlStatus

            try:
                dlStatus = "Downloading"
                r = self.download()
            except Exception as e:
                dlStatus = "Waiting"
                print(e)

            self.stop()

        def poweredDLPercentage(self, n=0, t=0):
            power = 1024
            power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
            perc = int(self.chunkCount * self.chunkSize)
            percTotal = int(self.totalSize)
            while perc > power:
                perc /= power
                n += 1
            while percTotal > power:
                percTotal /= power
                t += 1
            perc = "~" + str(round(perc, 1)) + power_labels[n]+"B"
            percTotal = str(round(percTotal, 1)) + power_labels[t]+"B"
            finalPerc = str(perc) + " / " + str(percTotal)
            return finalPerc

        def poweredDLTotal(self, n=0, t=0):
            power = 1024
            power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
            perc = int(self.chunkCount * self.chunkSize)
            while perc > power:
                perc /= power
                n += 1
            finalTotal = "~" + str(round(perc, 1)) + power_labels[n]+"B"
            return finalTotal

        def download(self):
            global dlPercentage, dlPercentageText
            global dlPercentageStatusText, dlPercentageActuallyPercentage
            global modScreen
            with self.url as getMod:
                if self.totalSize > 0:
                    dlPercentageActuallyPercentage = True
                    while dlPercentage < 100 and not self.stopped():
                        chunk = getMod.iter_content(self.chunkSize)
                        try:
                            chunk = next(chunk)
                        except StopIteration:
                            dlPercentageActuallyPercentage = True
                            break
                        self.chunkCount += 1
                        dlPercentage = int(self.chunkCount * self.chunkSize * 100 / self.totalSize)
                        dlPercentageText = int(dlPercentage)
                        dlPercentageStatusText = str(self.poweredDLPercentage())
                        self.fp.write(chunk)
                        if dlPercentage % 5 == 0:
                            renpy.restart_interaction()
                else:
                    dlPercentageActuallyPercentage = False
                    for chunk in getMod.iter_content(self.chunkSize):
                        if chunk:
                            self.chunkCount += 1
                            dlPercentage = int(self.chunkCount * self.chunkSize)
                            dlPercentageText = int(dlPercentage)
                            dlPercentageStatusText = "(" + str(self.poweredDLTotal()) + ")..."
                            self.fp.write(chunk)
                            if dlPercentage % 5 == 0:
                                renpy.restart_interaction()
            self.chunkCount = 0
            self.fp.close()