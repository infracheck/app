from typing import List

from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import IPluginData
from infracheck.model.ITestResult import IPluginResult, IModuleResult


class DemoPlugin(IPlugin):
    params = {}
    id = 'demo_plugin'
    version = 0.1
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

    def test(self, plugin_data: IPluginData) -> IPluginResult:
        """
        This is the demo test function

        :param plugin_data:
        :return:
        """
        module_result: List[IModuleResult] = []
        for module_data in plugin_data['modules']:
            module = self.get_module_by_id(module_data['id'])()
            for param in module.params.keys():
                module.params[param]['value'] = module_data['params'][param]
            module_result.append(module.test())

        result: IPluginResult = {
            "plugin_name": self.id,
            "plugin_version": self.version,
            "success_count": sum(c['is_successful'] for c in module_result),
            "failure_count": sum(not c['is_successful'] for c in module_result),
            "error_count": 0,
            "total_count": len(module_result),
            "message": "Hello World",
            "module_result": module_result,
            "custom_data": {}
        }
        return result
