
from typing import cast

from logging import Logger
from logging import getLogger

from core.types.Types import OglObjects

from plugins.io.gml.GMLExporter import GMLExporter

from core.IOPluginInterface import IOPluginInterface
from core.IPluginAdapter import IPluginAdapter

from core.types.PluginDataTypes import PluginName
from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import FormatName
from core.types.SingleFileRequestResponse import SingleFileRequestResponse


FORMAT_NAME:        FormatName = FormatName('GML')
PLUGIN_EXTENSION:   PluginExtension = PluginExtension('gml')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Graph Modeling Language - Portable Format for Graphs')


class IOGML(IOPluginInterface):
    """
    """
    def __init__(self, pluginAdapter: IPluginAdapter):
        """

        Args:
            pluginAdapter:   A class that implements IMediator
        """
        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name    = PluginName('Output GML')
        self._author  = "Humberto A. Sanchez II"
        self._version = GMLExporter.VERSION

        self._exportResponse: SingleFileRequestResponse = cast(SingleFileRequestResponse, None)

        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

    def setImportOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            if False, the import will be cancelled.
        """
        return False

    def setExportOptions(self) -> bool:
        """
        Prepare the export.

        Returns:
            if False, the export is cancelled.
        """
        self._exportResponse = self.askForFileToExport()

        if self._exportResponse.cancelled is True:
            return False
        else:
            return True

    def read(self) -> bool:
        """
        Read data from filename.
        """
        return False

    def write(self, oglObjects: OglObjects):
        """
        Write data

        Args:
            oglObjects:     list of exported objects
        """
        gmlExporter: GMLExporter = GMLExporter()

        gmlExporter.translate(umlObjects=oglObjects)

        gmlExporter.write(self._exportResponse.fileName)
