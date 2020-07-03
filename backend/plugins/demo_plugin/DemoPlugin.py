from typing import List

import xml.dom.minidom

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import IPluginData, IModuleData, IGeneralPluginData
from infracheck.model.ITestResult import TestResult

class TestInfraPluginData(IGeneralPluginData):
    hosts: List[str]
    username: str
    password: str


class DemoPlugin(IPlugin):
    id = 'demo_plugin'
    documentation = """
    ## Dulichium Victoria faciem Boeotia agris

Ait nisi: non ferar hostia orbis. Motis fama ademptae monstri nec utinamque
*soli* Paeonis praeceps Arethusa ab. Agmine iuvenis exarsit adunco manus, dea in
et atque: se erat, pingues.

    mbrNic = firmwareRuntimeAdware(logicIcon(crossplatform_multitasking,
            user_recursion + installer_agp_daemon, gif_bespoke_hover),
            dma_display_isa, bit_blu + sli_net_raid(dslamOffice,
            opticalMashup));
    ieee(page_scanner_spooling + utf_dual, 85, 79);
    veronica = partyUtfMegabit;
    var gigaflopsPptpCad = path(facebook, newbie_reader_cpl, 1);

## Ritus dea

Cortex ora quod, nate quae! **Non** se mihi salutant maternaque femina utinam si
obverterat ultor auferor. Agnorunt monstra cum quae insultavere efflant
praesenserat *Venus* effugit **Diomedis sopor** dereptis de excutior revocare
erit, concidere vocant. Est nobis, dum summas, sororum magnanimo *adhuc*:
miserrima et iter. Aquis ecce usus mandata suam.

> Oscula haec *Aetne*, et iterum abunde haud est leves silvaque, subiungit haec
> tacitorum illis, est felicia silvis. In urbem, Cerbere raptamque et **falli**,
> ad mora Dianae dedit vos. Nox cum haut arma brevis, et **sortitus tamen**,
> poenam.

## Oenides tamen

Cui lato omnia specus viae ista per agros nomen nascendi gratia est remotam
quodsi regia sed! Visus suos tota in rege, neque succurritis illa rotisque
Siculique latrantibus?

- Fecit virginis recentes
- Nurus nomen
- Memorare annos ut alii alumnus urebant artes
- Illinc feruntur

Non pectore arserunt, qua solent sanguine
*grandine cum cuius* ferrum sollertia curru limen nigrior raptores; sed mente.
Celebrant habetis stabis.

    """
    data: TestInfraPluginData = {
        "hosts": DataTypes.TextList,
        "username": DataTypes.Text,
        "target_os": DataTypes.Text,
        "password": DataTypes.Text,
        "port": DataTypes.Number
    }

    def test(self, _data: IPluginData) -> TestResult:
        return {"PLACEHOLDER": "PLACEHOLDER"}
