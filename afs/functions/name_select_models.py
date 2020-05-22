import logging
from arches.app.functions.base import BaseFunction
from arches.app.models import models
from arches.app.models.resource import Resource
from arches.app.models.graph import Graph
from arches.app.models.tile import Tile


details = {
    "name": "Name Selected Models",
    "type": "node",
    "description": "Names select models using tile data from related resource",
    "defaultconfig": {"selected_nodegroup": ""},
    "classname": "NameSelectModels",
    "component": "",
    "functionid": "577dbe09-11a6-4072-97d2-4f1a291dcda4",
}


class NameSelectModels(BaseFunction):
    select_models = {
        "ba892214-b25b-11e9-bf3e-a4d18cec433a": {  # visual work
            "name_nodeid": "d92f000a-c062-11e9-ab02-a4d18cec433a",
            "name_nodegroupid": "d92ef6c0-c062-11e9-bc19-a4d18cec433a",
            "related_nodeid": "5513933a-c062-11e9-9e4b-a4d18cec433a",  # related physical thing
            "related_nodegroupid": "5513933a-c062-11e9-9e4b-a4d18cec433a",
        },
        "707cbd78-ca7a-11e9-990b-a4d18cec433a": {  # digital resource
            "name_nodeid": "d2fdc2fa-ca7a-11e9-8ffb-a4d18cec433a",
            "name_nodegroupid": "d2fdae3d-ca7a-11e9-ad84-a4d18cec433a",
            "related_nodeid": "c1e732b0-ca7a-11e9-b369-a4d18cec433a",  # related visual work
            "related_nodegroupid": "c1e732b0-ca7a-11e9-b369-a4d18cec433a",
        },
    }

    def save(self, tile, request):
        def update_tile_name_node(tile, name_nodegroupid, name_nodeid, related_nodeid):
            # set tile for name using descriptor for rel resource
            related_resource_node_tile = Tile.objects.get(resourceinstance=tile.resourceinstance, nodegroup_id=related_nodeid)
            related_resource_id = related_resource_node_tile.data[related_nodeid][0]
            related_resource = Resource.objects.get(resourceinstanceid=related_resource_id)
            # create a new tile on the original resourceinstance concat "graph.name + 'of' + related_resource_name"
            new_tile = Tile()
            new_tile.nodegroup = models.NodeGroup.objects.get(nodegroupid=name_nodegroupid)
            new_tile.resourceinstance = tile.resourceinstance
            new_tile.data = {}
            new_tile.data[name_nodeid] = tile.resourceinstance.graph.name + " of " + related_resource.displayname
            new_tile.save()

        # check if its in the list of models I care about
        if str(tile.resourceinstance.graph.graphid) in list(self.select_models.keys()):
            # check the name node for a value, if empty: check appropriate related res node
            # g = tile.resourceinstance.graph
            name_nodegroupid = self.select_models[str(tile.resourceinstance.graph.graphid)]["name_nodegroupid"]
            # name_nodegroup = models.NodeGroup.objects.get(nodegroupid=)
            if not Tile.objects.filter(resourceinstance=tile.resourceinstance, nodegroup_id=name_nodegroupid).exists():
                # check appropriate rel res node
                related_nodegroupid = self.select_models[str(tile.resourceinstance.graph.graphid)]["related_nodegroupid"]
                if Tile.objects.filter(resourceinstance=tile.resourceinstance, nodegroup_id=related_nodegroupid).exists():
                    related_nodeid = self.select_models[str(tile.resourceinstance.graph.graphid)]["related_nodeid"]
                    name_nodeid = self.select_models[str(tile.resourceinstance.graph.graphid)]["name_nodeid"]
                    update_tile_name_node(tile, name_nodegroupid, name_nodeid, related_nodeid)

    def postSave(self, tile, request):
        raise NotImplementedError

    def on_import(self, tile):
        raise NotImplementedError

    def after_function_save(self, tile, request):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError