from petreader.labels import *
from petreader.TokenClassification import TokenClassification
from petreader.RelationsExtraction import RelationsExtraction
import networkx as nx
import matplotlib.pyplot as plt
# from pydata.graphs.savegraphs import SaveGraph
import os
from collections import defaultdict

BEHAVIORAL = 'b'
TYPE = 'type'
LABEL = 'label'

colors = {ACTIVITY: "skyblue",
          ACTIVITY_DATA: "yellow",
          ACTOR:    'red',
          AND_GATEWAY: 'black',
          XOR_GATEWAY: 'black',
          CONDITION_SPECIFICATION: 'black',

          FLOW:     'green',
          SAME_GATEWAY: 'red',
          USES: "yellow",
          ACTOR_PERFORMER: 'orange'}


def SaveGraph(graph: nx.Graph,
              outputfolder='./') -> None:
    """Save a graph into .dot and create .png and .pdf images of the graph

        graph is the nx graph
        outputfolder is the folder where results are saved
    """
    name = graph.name
    #  save graph in .dot
    nx.nx_agraph.write_dot(graph,  os.path.join(outputfolder, name) + '.dot')

    node_labels = dict()
    node_color_map = list()
    #  node attrs
    for node in graph.nodes:
        node_labels[node] = graph.nodes[node]['attrs'][LABEL]
        node_color_map.append(colors[graph.nodes[node]['attrs'][TYPE]])

    edge_labels = dict()
    edge_color_map = list()
    for edge in graph.edges:
        edge_labels[edge] = graph.edges[edge]['attrs'][TYPE]
        edge_color_map.append(colors[graph.edges[edge]['attrs'][TYPE]])


    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')

    plt.figure(figsize=(8, 8))
    # draw labels
    nx.draw_networkx_nodes(graph,
                           pos,
                           node_color=node_color_map,
                           node_size=500, #23,
                           alpha=0.35,
                           )
    # shifty = 1.50
    # shiftx = 0  # -70.0
    # pos_node_labels = {k: (p[0] + shiftx, p[1] + shifty) for k, p in pos.items()}
    nx.draw_networkx_labels(graph,
                            pos,  # _node_labels,
                            labels=node_labels,
                            horizontalalignment='center',
                            verticalalignment='center',  # 'bottom',
                            font_size=11,
                            font_weight='bold',
                            font_color='black')
    nx.draw_networkx_edges(graph,
                           pos,
                           edge_color=edge_color_map,
                           arrows=True,
                           arrowsize=13,
                           arrowstyle='->',
                           )
    nx.draw_networkx_edge_labels(graph,
                                 pos,
                                 edge_labels=edge_labels,
                                 font_size=8, #10,
                                 font_color='black')

    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.tight_layout()

    #   save fig before show it
    plt.savefig(os.path.join(outputfolder, name) + '.png',
                format='png', dpi=1000)
    plt.savefig(os.path.join(outputfolder, name) + '.pdf',
                format='pdf', dpi=1000)

    # warnings.warn('Show plot mode')
    plt.show()
    # plt.close('all')


class ProcessInformation:
    def __init__(self):
        self.tc = TokenClassification()
        self.rc = RelationsExtraction()

    def GetGateways(self,
                    doc_name: str):
        #  return the list of gateways and condition specification
        gateway_list =list()
        gateway_entities = list()

        doc_id = self.rc.GetDocumentNumber(doc_name)
        relations = self.rc.GetRelations(doc_id)[SAME_GATEWAY]
        print('here')
        assert False


    def GetActivityData(self,
                        doc_name: str):
        activity_data = list()
        activity_data_entities = list()
        doc_id = self.rc.GetDocumentNumber(doc_name)
        relations = self.rc.GetRelations(doc_id)[USES]

        for use_rel in relations:
            activity_node = (use_rel[SOURCE_SENTENCE_ID], use_rel[SOURCE_HEAD_TOKEN_ID])
            activity_label = ' '.join(use_rel[SOURCE_ENTITY])
            ad_node = (use_rel[TARGET_SENTENCE_ID], use_rel[TARGET_HEAD_TOKEN_ID])
            ad_label = ' '.join(use_rel[TARGET_ENTITY])

            activity_data.append((activity_node, ad_node))
            activity_data_entities.append((activity_label, ad_label))
        return activity_data, activity_data_entities

    def GetPerformsActors(self,
                          doc_name: str):
        performs = list()
        performs_entities = list()
        doc_id = self.rc.GetDocumentNumber(doc_name)
        activities = self.tc.GetActivities(doc_name)
        relations = self.rc.GetRelations(doc_id)[ACTOR_PERFORMER]

        for performs_rel in relations:
            activity_node = (performs_rel[SOURCE_SENTENCE_ID], performs_rel[SOURCE_HEAD_TOKEN_ID])
            activity_label = ' '.join(performs_rel[SOURCE_ENTITY])
            actor_node = (performs_rel[TARGET_SENTENCE_ID], performs_rel[TARGET_HEAD_TOKEN_ID])
            actor_label = ' '.join(performs_rel[TARGET_ENTITY])

            performs.append((activity_node, actor_node))
            performs_entities.append((activity_label, actor_label))
        return performs, performs_entities


    def GetKnowledgeGraph(self,
                          doc_name,
                          outputdir='./'):
        actors = self.GetKG_DFGPerformsActors(doc_name)
        act_data = self.GetKG_DFGActivityData(doc_name)

        combined = nx.DiGraph()

        combined.add_edges_from(actors.edges(data=True))
        combined.add_edges_from(act_data.edges(data=True))
        combined.add_nodes_from(actors.nodes(data=True))
        combined.add_nodes_from(act_data.nodes(data=True))  # deals with isolated nodes

        return combined

    def GetKG_DFGActivityData(self,
                                doc_name: str,
                                outputdir='./'):
        #  return a a graph
        graph = self.GetDFG(doc_name, outputdir=outputdir)

        doc_id = self.rc.GetDocumentNumber(doc_name)
        # activities = self.tc.GetActivities(doc_name)
        relations = self.rc.GetRelations(doc_id)[USES]

        for use_rel in relations:
            activity_node = (use_rel[SOURCE_SENTENCE_ID], use_rel[SOURCE_HEAD_TOKEN_ID])
            ad_node =  (use_rel[TARGET_SENTENCE_ID], use_rel[TARGET_HEAD_TOKEN_ID])
            graph.add_node(ad_node, attrs={TYPE: ACTIVITY_DATA, LABEL: ' '.join(use_rel[TARGET_ENTITY])})

            graph.add_edge(activity_node, ad_node, attrs={TYPE: USES, LABEL: USES})

        return graph

    def GetKG_DFGPerformsActors(self,
                                doc_name: str,
                                outputdir='./'):
        #  return a a graph
        graph = self.GetDFG(doc_name, outputdir=outputdir)

        doc_id = self.rc.GetDocumentNumber(doc_name)
        # activities = self.tc.GetActivities(doc_name)
        relations = self.rc.GetRelations(doc_id)[ACTOR_PERFORMER]

        for performs_rel in relations:
            activity_node = (performs_rel[SOURCE_SENTENCE_ID], performs_rel[SOURCE_HEAD_TOKEN_ID])
            actor_node =  (performs_rel[TARGET_SENTENCE_ID], performs_rel[TARGET_HEAD_TOKEN_ID])
            graph.add_node(actor_node, attrs={TYPE: ACTOR, LABEL: ' '.join(performs_rel[TARGET_ENTITY])})

            graph.add_edge(activity_node, actor_node, attrs={TYPE: ACTOR_PERFORMER, LABEL: ACTOR_PERFORMER})

        return graph


    def GetRawActivityLabels(self,
                             doc_name: str):
        #  store activity information (sentence, head word index, text)
        # activity_info = list()
        activity_info2 = dict()


        doc_id = self.rc.GetDocumentNumber(doc_name)
        # token classification sentence indexes
        tc_indexes = self.tc.get_n_sample_of_a_document(doc_name)
        process_description = self.tc.GetDocumentText(doc_name)
        #  get activities from TC
        activities = self.tc.GetActivities(doc_name)
        activities_indexes = self.tc.GetActivities(doc_name, True)

        for n_sent, (act_text, act_head_index) in enumerate(zip(activities, activities_indexes)):
            for act_, act_head in zip(act_text, act_head_index):
                # activity_info.append({SOURCE_SENTENCE_ID:n_sent,
                #                       SOURCE_HEAD_TOKEN_ID: act_head[0],
                #                       SOURCE_ENTITY: act_,
                #                       TEXT: [self.tc.GetTokens(tc_indexes[n_sent])],
                #                       RAW_LABEL: [act_],
                #                       ACTIVITY_DATA: list(),
                #                       FURTHER_SPECIFICATION: list()})

                key = (n_sent, act_head[0])
                activity_info2[key] = {PROCESS_DESCRIPTION: process_description,
                                       TEXT: ' '.join(self.tc.GetTokens(tc_indexes[n_sent])),
                                       RAW_LABEL: [act_],}
        #  get activities from RC
        # Get Activity + Activity Data for each activity in texts
        r = self.rc.GetRelations(doc_id)

        #  uses relation
        uses = r[USES]
        for use_rel in uses:
            print(use_rel)
            key = (use_rel[SOURCE_SENTENCE_ID], use_rel[SOURCE_HEAD_TOKEN_ID])

            if use_rel[SOURCE_SENTENCE_ID] != use_rel[TARGET_SENTENCE_ID]:
                #  add text
                target_text = ' '.join(self.tc.GetTokens(tc_indexes[use_rel[TARGET_SENTENCE_ID]]))

                if use_rel[SOURCE_SENTENCE_ID] < use_rel[TARGET_SENTENCE_ID]:
                    activity_info2[key][TEXT] = activity_info2[key][TEXT] + target_text
                    activity_info2[key][RAW_LABEL].append(use_rel[TARGET_ENTITY])

                else:
                    #  use_rel[SOURCE_SENTENCE_ID] > use_rel[TARGET_SENTENCE_ID]:
                    activity_info2[key][TEXT] = target_text + activity_info2[key][TEXT]
                    activity_info2[key][RAW_LABEL].insert(0, use_rel[TARGET_ENTITY])
            else:
                # text is the same
                if use_rel[SOURCE_HEAD_TOKEN_ID] < use_rel[TARGET_HEAD_TOKEN_ID]:
                    # append activity data
                    activity_info2[key][RAW_LABEL].append(use_rel[TARGET_ENTITY])
                else:
                    # insert activity data before activity
                    activity_info2[key][RAW_LABEL].insert(0, use_rel[TARGET_ENTITY])
        # print(activity_info2)
        # print()
        return activity_info2

    def GetDFG(self,
               doc_name: str,
               outputdir='./'):
        graph = self.construct_behavioral_graph(doc_name)
        SaveGraph(graph, outputfolder=outputdir)

        graph = self.construct_dfg(graph)
        SaveGraph(graph, outputfolder=outputdir)

        return graph


    def construct_behavioral_graph(self, doc_name):
        #  returns:
        #       a nx graph representing behavioral elements (ACTIVITY, GATEWAY, CONDITION SPECIFICATION)
        #       a dict(node code)= {type: Act/Gate/CondSpec, label: str}
        #       a dict(edge) = edge type: str

        graph = nx.DiGraph()
        graph.name = doc_name
        # node_dict = dict()
        # edges_dict = dict()
        doc_id = self.rc.GetDocumentNumber(doc_name)

        #  add flow  Relations
        relations = self.rc.GetRelations(doc_id)[FLOW]
        for rel in relations:
            source_key = (rel[SOURCE_SENTENCE_ID], rel[SOURCE_HEAD_TOKEN_ID])
            target_key = (rel[TARGET_SENTENCE_ID], rel[TARGET_HEAD_TOKEN_ID])

            graph.add_edge(source_key, target_key, attrs={TYPE: FLOW})
            graph.add_node(source_key, attrs={TYPE: rel[SOURCE_ENTITY_TYPE], LABEL: ' '.join(rel[SOURCE_ENTITY])})
            graph.add_node(target_key, attrs={TYPE: rel[TARGET_ENTITY_TYPE], LABEL: ' '.join(rel[TARGET_ENTITY])})

        #  add Same Gateway Relation
        relations = self.rc.GetRelations(doc_id)[SAME_GATEWAY]
        for rel in relations:
            source_key = (rel[SOURCE_SENTENCE_ID], rel[SOURCE_HEAD_TOKEN_ID])
            target_key = (rel[TARGET_SENTENCE_ID], rel[TARGET_HEAD_TOKEN_ID])

            graph.add_edge(source_key, target_key, attrs={TYPE: SAME_GATEWAY})
            graph.add_node(source_key, attrs={TYPE: rel[SOURCE_ENTITY_TYPE], LABEL: ' '.join(rel[SOURCE_ENTITY])})
            graph.add_node(target_key, attrs={TYPE: rel[TARGET_ENTITY_TYPE], LABEL: ' '.join(rel[TARGET_ENTITY])})

        return graph

    def construct_dfg(self, graph):

        graph.name = '{}-{}'.format('Directly Folows Graph', graph.name)

        #  remove non activity nodes and edges
        nodes_to_be_removed = list()
        for node in graph.nodes:
            predecessors = list(graph.predecessors(node))
            successors = list(graph.successors(node))
            if graph.nodes[node]['attrs'][TYPE] != ACTIVITY:
                if predecessors:
                    for pred in predecessors:
                        for succ in successors:
                            graph.add_edge(pred, succ, attrs={TYPE: FLOW})
                nodes_to_be_removed.append(node)
        [graph.remove_node(n) for n in nodes_to_be_removed]

        return graph


if __name__ == '__main__':
    from pprint import pprint
    pi = ProcessInformation()
    doc_name = 'doc-1.3'
    SaveGraph(pi.GetKnowledgeGraph(doc_name))
    print()
    # SaveGraph(pi.GetKG_DFGActivityData(doc_name))
    # pprint(pi.GetActivityData(doc_name))
    # pprint(pi.GetRawActivityLabels(doc_name))
    # print()
    # pi.GetDFG(doc_name)
    # print()
    # SaveGraph(pi.GetKG_DFGPerformsActors(doc_name))
    # print()
    # pprint(pi.GetPerformsActors(doc_name))
    # print()
