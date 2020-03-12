from act.scio.attrdict import AttrDict
from act.scio.vocabulary import Vocabulary
from act.scio.plugin import BasePlugin, Result
from typing import Text, List
import configparser
import logging
import os.path


class Plugin(BasePlugin):
    name = "tools"
    info = "Extracting references to known tools from a body of text"
    version = "0.1"
    dependencies: List[Text] = []

    async def analyze(self, text: Text, prior_result: AttrDict) -> Result:

        ini = configparser.ConfigParser()
        ini.read([os.path.join(self.configdir, "tools_pattern.ini")])
        ini['tools']['alias'] = os.path.join(self.configdir, ini['tools']['alias'])

        vocab = Vocabulary(AttrDict(ini['tools']))

        tas = []
        for regex in vocab.regex:
            for match in regex.findall(text):
                tas.append(match)
                if self.debug:
                    logging.info("%s found by regex %s", match, regex)

        res = AttrDict()

        res.Tools = tas

        return Result(name=self.name, version=self.version, result=res)
