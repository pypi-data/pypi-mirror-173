from tqdm import tqdm
from sklearn.model_selection import KFold
from sklearn.linear_model import OrthogonalMatchingPursuitCV
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
import networkx.algorithms.community as nx_comm
import networkx as nx
from os.path import join
import seaborn as sns
import gseapy as gp
from copy import deepcopy
import matplotlib.pyplot as plt
from gseapy.plot import gseaplot, heatmap
from GXN.data.GO.go_loader import load_go
from goatools.mapslim import mapslim
from goatools.go_enrichment import GOEnrichmentStudy
from kneed import KneeLocator
from sklearn.svm import LinearSVR
from sklearn.svm import l1_min_c
import pickle as p
import os

class __General_GXN__:
    def __init__(self, predictor, **predictor_parameters):
        '''
        Object that infer a GXN from gene expression data, using a
        predifined predictor
        '''
        self.predictor = predictor
        self.predictor_parameters = predictor_parameters
        self.C = None
        self.C_non_refined = None
        self.G = None
        self.communities = None
        self.GSEA = None
        self.ododag = load_go(False)
        self.ododag_slim = load_go(True)
        self.community_label = 'C'
        self.GO = None
        self.model_per_gene = None
        self.tfs_per_tg = None
        self.model_evaluations = None
        self.suitable_models_ratio = None
        self.sparsity = None
        self.modularity = None
        self.communities_descriptions = None
        self.rolling_multi_resolution = None
        self.kn = None

    def save(self,folder):
        p.dump(self.predictor, open(join(folder,"predictor.pickle"),"wb"))
        p.dump(self.predictor_parameters, open(join(folder,"predictor_parameters.pickle"),"wb"))
        p.dump(self.C, open(join(folder,"C.pickle"),"wb"))
        p.dump(self.C_non_refined, open(join(folder,"C_non_refined.pickle"),"wb"))
        p.dump(self.G, open(join(folder,"G.pickle"),"wb"))
        p.dump(self.communities, open(join(folder,"communities.pickle"),"wb"))
        p.dump(self.GSEA, open(join(folder,"GSEA.pickle"),"wb"))
        p.dump(self.community_label, open(join(folder,"community_label.pickle"),"wb"))
        p.dump(self.GO, open(join(folder,"GO.pickle"),"wb"))
        p.dump(self.model_per_gene, open(join(folder,"model_per_gene.pickle"),"wb"))
        p.dump(self.tfs_per_tg, open(join(folder,"tfs_per_tg.pickle"),"wb"))
        p.dump(self.model_evaluations, open(join(folder,"model_evaluations.pickle"),"wb"))
        p.dump(self.suitable_models_ratio, open(join(folder,"suitable_models_ratio.pickle"),"wb"))
        p.dump(self.sparsity, open(join(folder,"sparsity.pickle"),"wb"))
        p.dump(self.modularity, open(join(folder,"modularity.pickle"),"wb"))
        p.dump(self.communities_descriptions, open(join(folder,"communities_descriptions.pickle"),"wb"))
        p.dump(self.rolling_multi_resolution, open(join(folder,"rolling_multi_resolution.pickle"),"wb"))
        p.dump(self.kn, open(join(folder,"kn.pickle"),"wb"))


    def load(self,folder):
        self.predictor = p.load(open(join(folder,"predictor.pickle"),"rb"))
        self.predictor_parameters = p.load(open(join(folder,"predictor_parameters.pickle"),"rb"))
        self.C = p.load(open(join(folder,"C.pickle"),"rb"))
        self.C_non_refined = p.load(open(join(folder,"C_non_refined.pickle"),"rb"))
        self.G = p.load(open(join(folder,"G.pickle"),"rb"))
        self.communities = p.load(open(join(folder,"communities.pickle"),"rb"))
        self.GSEA = p.load(open(join(folder,"GSEA.pickle"),"rb"))
        self.community_label = p.load(open(join(folder,"community_label.pickle"),"rb"))
        self.GO = p.load(open(join(folder,"GO.pickle"),"rb"))
        self.model_per_gene = p.load(open(join(folder,"model_per_gene.pickle"),"rb"))
        self.tfs_per_tg = p.load(open(join(folder,"tfs_per_tg.pickle"),"rb"))
        self.model_evaluations = p.load(open(join(folder,"model_evaluations.pickle"),"rb"))
        self.suitable_models_ratio = p.load(open(join(folder,"suitable_models_ratio.pickle"),"rb"))
        self.sparsity = p.load(open(join(folder,"sparsity.pickle"),"rb"))
        self.modularity = p.load(open(join(folder,"modularity.pickle"),"rb"))
        self.communities_descriptions = p.load(open(join(folder,"communities_descriptions.pickle"),"rb"))
        self.rolling_multi_resolution = p.load(open(join(folder,"rolling_multi_resolution.pickle"),"rb"))
        self.kn = p.load(open(join(folder,"kn.pickle"),"rb"))

    def feature_importance_function(self,predictor):
        '''
        Compute and return feature importance of inner predictor

        Returns:
            numpy.array: importance scores for each feature

        '''
        if hasattr(predictor, 'feature_importances_'):
            return predictor.feature_importances_
        elif hasattr(predictor,"coef_"):
            if len(predictor.coef_.shape) > 1:
                return np.abs(predictor.coef_).mean(axis=0)
            else:
                return np.abs(predictor.coef_.flatten())


    def fit_predict(self,
                    gene_expression_matrix,
                    tf_list = None,
                    tg_list = None,
                    progress_bar=False,
                    cv=KFold(n_splits=5, shuffle=True, random_state=33)):
        """
        Scores transcription factors-target gene co-expressions using a predictor.

        Args:
            gene_expression_matrix (pandas.DataFrame):  gene expression matrix where
                rows are samples (conditions) and  columns ares genes.
                The value at row i and column j represents the expression of gene i
                in condition j.
            tf_list (list or numpy.array): list of transcription factors ids.
            tg_list (list or numpy.array): list of target genes ids.
            normalize (boolean): If True the gene expression of genes is z-scored
            progress_bar: bool, if true include progress bar
            cv: int, cross-validation generator or an iterable, default=None
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are those of GridSearchCV  from sklearn

        Returns:
            pandas.DataFrame: GXN scores matrix.
            dict: Dictionnary with genes as keys and models as values
            pandas.DataFrame: Summary of TG predictors evaluations

            Rows are target genes and columns are transcription factors.
            The value at row i and column j represents the score assigned by the
            score_predictor to the regulatory relationship between target gene i
            and transcription factor j.

        """
        if tg_list is None:
            tg_list = gene_expression_matrix.columns
        if tf_list is None:
            tf_list = gene_expression_matrix.columns
        tf_list_present = set(gene_expression_matrix.columns).intersection(tf_list)
        tg_list_present = list(set(gene_expression_matrix.columns).intersection(tg_list))

        if not len(tf_list_present):
            Exception('None of the tfs in '+str(tf_list)+\
            " is present in the gene_expression_matrix genes list"+\
            str(gene_expression_matrix.columns))
        if not len(tg_list_present):
            Exception('None of the tgs in '+str(tg_list)+\
            " is present in the gene_expression_matrix genes list"+\
            str(gene_expression_matrix.columns))
        tg_list_present.sort()

        # compute tf scores for each gene
        scores_tf_per_gene = []
        self.model_per_gene = {}
        self.tfs_per_tg = {}
        for gene in tqdm(tg_list_present,disable=not progress_bar):
            # Exclude the current gene from the tfs list
            tfs2test = list(tf_list_present.difference(set([gene])))
            self.tfs_per_tg[gene] = tfs2test
            X = gene_expression_matrix[tfs2test].values
            y = gene_expression_matrix[gene].values
            clf = GridSearchCV(self.predictor,
                               self.predictor_parameters,
                               n_jobs=1,
                               cv=cv,
                               verbose=0)
            clf.fit(X,y)
            score = self.feature_importance_function(clf.best_estimator_)
            self.model_per_gene[gene] = clf
            scores = pd.Series(score,index=tfs2test)
            scores_tf_per_gene.append(scores)
        df_results = pd.DataFrame(scores_tf_per_gene, index=tg_list_present)
        self.C = df_results
        self.C_non_refined = deepcopy(self.C)
        evaluation_features = [ "mean_test_score",
                                'std_test_score',
                                "mean_fit_time",
                                "std_fit_time",
                                "mean_score_time",
                                "std_score_time"]
        model_evaluations = {}
        for tg in self.model_per_gene:
            model_evaluations[tg] = {f:self.model_per_gene[tg].cv_results_[f][0] for f in evaluation_features}
        self.model_evaluations = pd.DataFrame(model_evaluations).T

        return(self.C, self.model_per_gene, self.model_evaluations)

    def score(self,
                gene_expression_matrix,
                tg_list = None,
                progress_bar=False,):
        if tg_list is None:
            tg_list = gene_expression_matrix.columns
        tg_list_present = list(set(gene_expression_matrix.columns).intersection(tg_list))
        tg_list_present = list(set(tg_list_present).intersection(list(self.tfs_per_tg.keys())))
        if self.C is not None:
            scores = {}
            for gene in tqdm(tg_list_present,disable=not progress_bar):
                # Exclude the current gene from the tfs list
                tfs2test = self.tfs_per_tg[gene]
                X = gene_expression_matrix[tfs2test].values
                y = gene_expression_matrix[gene].values
                clf = self.model_per_gene[gene].best_estimator_
                scores[gene] = clf.score(X,y)
            scores = pd.Series(scores)
            return(scores)
        else:
            print("Please use the fit_predict to create a GXN before using this function")


    def predict(self,
                gene_expression_matrix,
                tg_list = None,
                progress_bar=False,):
        if tg_list is None:
            tg_list = gene_expression_matrix.columns
        tg_list_present = list(set(gene_expression_matrix.columns).intersection(tg_list))
        tg_list_present = list(set(tg_list_present).intersection(list(self.tfs_per_tg.keys())))
        if self.C is not None:
            predictions = {}
            for gene in tqdm(tg_list_present,disable=not progress_bar):
                # Exclude the current gene from the tfs list
                tfs2test = self.tfs_per_tg[gene]
                X = gene_expression_matrix[tfs2test].values
                y = gene_expression_matrix[gene].values
                clf = self.model_per_gene[gene].best_estimator_
                predictions[gene] = pd.Series(clf.predict(X),
                                    index=gene_expression_matrix.index)
            predictions = pd.DataFrame(predictions)
            return(predictions)
        else:
            print("Please use the fit_predict to create a GXN before using this function")

    def refine_C(self,R2_threshold=0.5):
        """
        Remove all TGs for which it was not possible to build a suitable regression
        model (validation R2 score lower than a threshold) are removed from the
        coefficient matrix $C$, as well as all the TFs that have never been used
        in a regression model

        Args:
            R2_threshold (float): validation R2 score threshold.

        """
        if self.C is not None:
            self.C = deepcopy(self.C_non_refined)
            correct_tgs = self.model_evaluations["mean_test_score"]>R2_threshold
            C = self.C.loc[correct_tgs[correct_tgs].index]
            used_tfs = np.abs(C).sum()>0
            C = C.T[used_tfs].T
            self.C = C
        else:
            print("Please use the fit_predict to create a GXN before using this function")

    def compute_suitable_models_ratio(self,R2_threshold=0.5):
        """
        Compute the ratio of models that have an R2 validation score higher than
        a given threshold (and thus considered as suitable)

        Args:
            R2_threshold (float): validation R2 score threshold.

        Returns:
            float: ratio (between 0 and 1) of suitable models
        """
        if self.C is not None:
            nb_correct_models = (self.model_evaluations["mean_test_score"]>R2_threshold).sum()
            self.suitable_models_ratio = nb_correct_models/len(self.model_evaluations.index)
            return self.suitable_models_ratio
        else:
            print("Please use the fit_predict to create a GXN before using this function")

    def compute_sparsity(self):
        """
        Compute the sparsity of the GXN model (number of actual links/number of possible links)
        here self loops are not considered.

        Returns:
            float: sparsity level (between 0 and 1)
        """

        if self.C is not None:
            nb_genes = len(self.C.columns)
            nb_tfs = len(self.C.index)
            full_connections = (nb_genes-1)*nb_tfs
            self.sparsity = (self.C.fillna(0)!=0).sum(axis=0).sum()/full_connections
            return self.sparsity
        else:
            print("Please use the fit_predict to create a GXN before using this function")

    def __C_to_edge_list(self):
        if self.C is not None:
            A = self.C.fillna(0)
            A_unsktack = A.unstack(level=0)
            A_unsktack = A_unsktack[A_unsktack!=0]
            edge_list = A_unsktack.reset_index()
            edge_list.columns = ["TF","TG","Score"]
            edge_list["AbsScore"] = np.abs(edge_list["Score"])
            return edge_list
        else:
            print("Please use the fit_predict to create a GXN before using this function")

    def get_networkx_graph(self):
        """
        Return the GXN (stored as a matrix coefficient $C$), as a networkx directed graph

        Returns:
            networkx.DiGraph: the networkx graph associated to the GXN model
        """
        if self.C is not None:
            edge_list = self.__C_to_edge_list()
            self.G = nx.from_pandas_edgelist(edge_list,
                                            source='TF',
                                            target='TG',
                                            edge_attr=["Score","AbsScore"],
                                            create_using=nx.DiGraph())
            return self.G
        else:
            print("Please use the fit_predict to create a GXN before using this function")

    def get_communities(self,weights="Score",resolution=1,label="C"):

        if self.C is not None:
            self.get_networkx_graph()
            self.communities = list(nx_comm.greedy_modularity_communities(self.G,
                                                                          resolution=resolution,
                                                                          weight=weights))
            self.community_label = label
        else:
            print("Please use the fit_predict to create a GXN before using this function")

    def compute_modularity(self,resolution=1):
        if self.communities is None:
            self.get_communities()
        self.modularity = nx_comm.modularity(self.G.to_undirected(),
                                             self.communities,
                                             resolution=resolution,
                                             weight="Score")
        return self.modularity

    def plot_community(self,id_community,threshold=0.2,prog="neato",labels=True):
        if self.communities is None:
            self.get_communities()
        community = self.communities[id_community]
        grn_inferred_community = self.G.subgraph(community).copy()
        self.plot_network(grn_inferred_community,threshold,prog,labels)

    def plot_network(self,graph,threshold=0.2,prog="neato",labels=True):
        graph = graph.copy()
        colnodes = []
        graph.remove_edges_from([(n1, n2) for n1, n2, w in graph.edges(data="Score") if np.abs(w) < threshold])
        graph.remove_nodes_from(list(nx.isolates(graph)))

        for node in graph:
            colnodes.append('cadetBlue')

        # Define scores for the edge colors as 1/(log(rank)+1)
        edge_colors = []
        for edge in graph.edges():
            s = graph[edge[0]][edge[1]]["Score"]
            edge_colors.append(s)#np.log(grn_inferred_community[edge[0]][edge[1]]["rank"]+1))

        # Define the fire size
        plt.figure(figsize=(10,10))

        # Define the node size prop. to its degree
        nodes_degrees = dict(graph.degree)

        # Plot the network
        # neato, dot, twopi, circo, fdp, sfdp.
        nx.draw(graph,edge_cmap=plt.cm.coolwarm,#RdYlBu,
                pos = nx.nx_agraph.graphviz_layout(graph,prog=prog),
                node_color=colnodes,edge_color = edge_colors,edge_vmin=-1.,edge_vmax=1,
                with_labels = labels,alpha=0.9,font_size=7,#font_weight="bold",
                arrowsize=10, arrowstyle='fancy',node_shape="o",width=1,
                node_size=[np.log(nodes_degrees[k]+1)*100 for k in nodes_degrees])


    def gsea_analysis(self,gene_expression_matrix,tissues,**gsea_params):
        if self.C is None:
            print("Please use the fit_predict to create a GXN before using this function")
            return
        if self.communities is None:
            self.get_communities()
        gsea_base_params = {'method':"diff_of_classes",
                            'permutation_num':1000,
                            'min_size':10,
                            'max_size':1000,
                            'ascending':False,
                            'seed':33,
                            'verbose':True,
                            'outdir':None,
                            'permutation_type':'gene_set'}
        gsea_base_params.update(gsea_params)
        x = gene_expression_matrix
        gseq_res = {}
        for tissue in np.unique(tissues):
            print(tissue)
            x_local = pd.concat((x[tissues[tissues==tissue].dropna().index],
                                 x[tissues[tissues!=tissue].dropna().index]),axis=1)
            class_vector = []
            for c in x_local.columns:
                if tissues[c]==tissue:
                    class_vector.append(tissue)
                else:
                    class_vector.append("Other")
            gene_sets = {self.community_label+str(i):list(cc) for i,cc in enumerate(self.communities)}
            gseq_res[tissue] = gp.gsea(data=x_local,
                                       gene_sets=gene_sets,
                                       cls=class_vector,
                                       **gsea_base_params)
        self.GSEA = gseq_res

    def plot_gsea_curve(self, tissue, community):
        if self.C is None:
            print("Please use the fit_predict to create a GXN before using this function")
            return
        if self.GSEA is None:
            print("Please use the gsea_analysis to run a GSEA analysis before using this function")
            return
        term = self.community_label+str(community)
        gseaplot(self.GSEA[tissue].ranking,
                 term=term,
                 **self.GSEA[tissue].results[term])

    def filter_gsea(self,fdr_threshold=0.001,p_val_threshold=0.001):
        if self.C is None:
            print("Please use the fit_predict to create a GXN before using this function")
            return
        if self.GSEA is None:
            print("Please use the gsea_analysis to run a GSEA analysis before using this function")
            return
        gsea_M = {}
        gsea_fdr = {}
        gsea_pval = {}
        gsea_G = nx.Graph()
        for tissue in self.GSEA:
            gsea_M[tissue] = {}
            gsea_fdr[tissue] = {}
            gsea_pval[tissue] = {}
            m = self.GSEA[tissue].res2d.fillna(0)
            for gs in m.index:
                if m.loc[gs]["fdr"] <= fdr_threshold and m.loc[gs]["pval"] <= p_val_threshold:
                    nes = m.loc[gs]["nes"]
                    if np.isinf(nes):
                        nes = nes * np.sign(m.loc[gs]["es"])
                    gsea_G.add_edge(tissue, gs, nes= nes, fdr=m.loc[gs]["fdr"], pval=m.loc[gs]["pval"])
                gsea_M[tissue][gs] = m.loc[gs]["nes"]
                gsea_fdr[tissue][gs] = m.loc[gs]["fdr"]
                gsea_pval[tissue][gs] = m.loc[gs]["pval"]
        return gsea_M,gsea_fdr,gsea_pval,gsea_G

    def go_analysis(self,geneid2go_dict,p_fdr_bh_threshold=1e-3,**go_enrichment_params):

        go_enrichment_params_base = {'propagate_counts':False,
                                     "alpha":0.05,
                                     "methods":["fdr_bh"]}
        go_enrichment_params_base.update(go_enrichment_params)
        goeaobj = GOEnrichmentStudy(geneid2go_dict.keys(), # List of protein-coding genes
                                    geneid2go_dict, # geneid/GO associations
                                    self.ododag,
                                    **go_enrichment_params_base)
        self.GO = []
        groups = {self.community_label+str(i):list(cc) for i,cc in enumerate(self.communities)}
        for g in tqdm(groups):
            genes = groups[g]
            goea_results_all = goeaobj.run_study(genes,prt=None)#
            goea_results_sig = [r for r in goea_results_all if r.p_fdr_bh < p_fdr_bh_threshold]
            enriched = [{"community":g,
                         "GO":r.GO,
                         "Name":r.name,
                         "p_uncorrected":r.p_uncorrected,
                         "p_corrected":r.p_fdr_bh} for r in goea_results_sig if r.enrichment=='e']
            self.GO += enriched
        self.GO = pd.DataFrame(self.GO)
        return self.GO

    def get_GO_graph(self, term='GO:0048856', p_corrected_threshold=1e-2):#0060249

        results_filter = self.GO[[term in mapslim(go,self.ododag,self.ododag_slim)[1] for go in self.GO["GO"]]]
        results_filter = results_filter[results_filter["p_corrected"]<p_corrected_threshold]
        results_filter["score"] = -np.log10(results_filter["p_corrected"])

        def clean_txt(txt):
            txt = txt.lower()
            txt = "dev.".join(txt.split("development"))
            txt = "sys. ".join(txt.split("system "))
            txt = "\n".join(txt.split())
            return txt.title()


        GO_graph = nx.Graph()
        for idx in results_filter.index:
            GO_graph.add_edge(results_filter.loc[idx,"community"],
                              clean_txt(results_filter.loc[idx,"Name"]),
                              score=results_filter.loc[idx,"score"])
        return GO_graph

    def plot_go_goas_network(self,G,**visual_parameters):
        # Define the fire size
        nb_nodes = len(G.nodes)
        communities = [self.community_label+str(c) for c in range(len(self.communities))]
        visual_params_default = {"figsize":(1.3*int(np.sqrt(nb_nodes)),
                                            1.3*int(np.sqrt(nb_nodes))),
                                 "prog":"dot",
                                 "edge_cmap":plt.cm.coolwarm,
                                 "communities_color":"navajowhite",
                                 "GOs_color":"lavender",
                                 "GSEAs_color":"lightseagreen",
                                 "communities_nodes_size":10,
                                 "GOs_nodes_size":7,
                                 "GSEAs_nodes_size":7,
                                 "edge_vmin":-3,
                                 "edge_vmax":3,
                                 "with_labels":True,
                                 "alpha":0.9,
                                 "font_weight":"normal",#bold
                                 "arrowsize":10,
                                 "arrowstyle":"fancy",
                                 "node_shape":"o",
                                 'width':2,
                                 "node_size_scale":200,
                                 "bbox":{'boxstyle':'round',
                                         'ec':(1.0, 1.0, 1.0),
                                         'fc':(1.0, 1.0, 1.0),
                                         'alpha':0.2},
                                 "edge_label_alpha":0.6,
                                 "edge_label_font_size":6,
                                 }
        visual_params_default.update(visual_parameters)
        colnodes = []
        font_size = []
        for node in G:
            if node in communities:
                colnodes.append(visual_params_default["communities_color"])
                font_size.append(visual_params_default["communities_nodes_size"])
            elif self.GSEA is not None and node in list(self.GSEA.keys()):
                colnodes.append(visual_params_default["GSEAs_color"])
                font_size.append(visual_params_default["GSEAs_nodes_size"])
            else:
                colnodes.append(visual_params_default["GOs_color"])
                font_size.append(visual_params_default["GOs_nodes_size"])

        edge_colors = []
        edge_labels = {}
        for edge in G.edges():
            s=0
            if "score" in G[edge[0]][edge[1]]:
                s = G[edge[0]][edge[1]]["score"]
                edge_labels[edge] = str(np.round(G[edge[0]][edge[1]]["score"],1))
            elif "nes" in G[edge[0]][edge[1]]:
                s = G[edge[0]][edge[1]]["nes"]
                edge_labels[edge] = str(np.round(G[edge[0]][edge[1]]["nes"],1))
            elif "weight" in G[edge[0]][edge[1]]:
                s = G[edge[0]][edge[1]]["weight"]
                edge_labels[edge] = str(np.round(G[edge[0]][edge[1]]["weight"],1))
            edge_colors.append(s)

        # Define the node size prop. to its degree
        nodes_degrees = dict(G.degree)
        node_sizes = [(nodes_degrees[k]+1)*visual_params_default["node_size_scale"] for k in nodes_degrees]

        # Plot the network
        # neato, dot, twopi, circo, fdp, sfdp.
        pos = nx.nx_agraph.graphviz_layout(G,prog=visual_params_default["prog"])

        plt.figure(figsize=visual_params_default["figsize"])
        nx.draw(G,pos = pos, edge_cmap=visual_params_default["edge_cmap"],#RdYlBu,
                node_color=colnodes,edge_color=edge_colors,
                edge_vmin=visual_params_default["edge_vmin"],
                edge_vmax=visual_params_default["edge_vmax"],
                with_labels=visual_params_default["with_labels"],
                alpha=visual_params_default["alpha"],
                font_size=0,
                arrowsize=visual_params_default["arrowsize"],
                arrowstyle=visual_params_default["arrowstyle"],
                node_shape=visual_params_default["node_shape"],
                width=visual_params_default["width"],
                node_size=node_sizes,

                )
        i=0
        for node, (x, y) in pos.items():
            plt.text(x, y, node, fontsize=font_size[i], ha='center', va='center')
            i+=1

        nx.draw_networkx_edge_labels(G,pos,
                                    edge_labels=edge_labels,
                                    font_size=visual_params_default["edge_label_font_size"],
                                    alpha=visual_params_default["edge_label_alpha"],
                                    bbox=visual_params_default["bbox"])


    def get_GSEA_GO_network(self, GSEA_graph, GO_graph):
        common_nodes = set(GSEA_graph.nodes()).intersection(GO_graph.nodes())
        g = nx.Graph()
        for c in common_nodes:
            for e in GSEA_graph.edges(c):
                g.add_edge(e[0],e[1],weight=np.round(GSEA_graph.get_edge_data(*list(e))["nes"],2))
            for e in GO_graph.edges(c):
                g.add_edge(e[0],e[1],weight=np.round(GO_graph.get_edge_data(*list(e))["score"],2))
        return g


    def results_summary(self,features_custom=[]):
        ZERO = 1e-10
        features = ["mean_test_score",
                    'std_test_score',
                    "mean_fit_time",
                    "std_fit_time",
                    "mean_score_time",
                    "std_score_time"]
        feature = list(set(features+features_custom))
        results = {}
        for tg in self.model_per_gene:
            results[tg] = {f:self.model_per_gene[tg].cv_results_[f][0] for f in features}
            results[tg]["non_zero"] = (np.abs(self.C_non_refined.loc[tg])>ZERO).sum()
        results = pd.DataFrame(results).T
        return results

    def get_gene_communities_membership(self):
        communities_membership = {}
        for i,c in enumerate(self.communities):
            for gene in list(c):
                communities_membership[gene] = i
        for gene in self.C_non_refined.index:
            if gene not in communities_membership:
                communities_membership[gene] = -1
        return(pd.Series(communities_membership))

    def community_heatmap_average_per_tissue(self,X,tissue,community,**clustermap_params):
        X_community_avg = X[self.communities[community]].groupby(tissue).mean()
        clustermap_params_ = {"cmap":"coolwarm","center":0,"annot":True}
        clustermap_params_.update(clustermap_params)
        sns.clustermap(X_community_avg.T,**clustermap_params_)

    def compute_intra_community_sse(self,X,community):
        c = self.communities[community]
        X_community = X[c]
        sse = (X_community.var(axis=1)*X_community.shape[1]).sum()
        return sse

    def get_community_description(self,X,community):
        sse = self.compute_intra_community_sse(X,community)
        nb_nodes = len(self.communities[community])
        return {"SSE":sse, "Nb nodes":nb_nodes}

    def get_communities_description(self,X):
        descriptions = {}
        for i,c in enumerate(self.communities):
            descriptions[i] = self.get_community_description(X,i)
        return pd.DataFrame(descriptions).T

    def community_multi_resolution_analysis(self,
                                            X,
                                            resolutions=np.arange(0.5,5,0.25),
                                            rolling_average_window=5,
                                            **KneeLocator_params):
        side_points = rolling_average_window//2
        lside_vector = [min(resolutions)-(i+1)*0.1 for i in range(side_points)]
        rside_vector = [max(resolutions)+(i+1)*0.1 for i in range(side_points)]
        resolutions_ = lside_vector+list(resolutions)+rside_vector
        KneeLocator_params_default = {"curve":'convex',
                                      "direction":'decreasing',
                                      "S":100}
        KneeLocator_params_default.update(KneeLocator_params)
        communities_descriptions = []
        for r in tqdm(resolutions_):
            self.get_communities(weights="Score",resolution=r)
            description = self.get_communities_description(X)
            description["resolution"] = r
            communities_descriptions.append(description)
        communities_descriptions = pd.concat(communities_descriptions)
        rolling_multi_resolution = communities_descriptions.groupby("resolution").mean().rolling(rolling_average_window,center=True).mean().dropna()
        kn = self.communities_knee_locator(rolling_multi_resolution,**KneeLocator_params_default)
        communities_descriptions = communities_descriptions[communities_descriptions["resolution"].isin(resolutions)]
        self.communities_descriptions = communities_descriptions
        self.rolling_multi_resolution = rolling_multi_resolution
        self.kn = kn
        return communities_descriptions,rolling_multi_resolution,list(kn.all_knees)

    def communities_knee_locator(self,
                                 communities_descriptions,
                                 **KneeLocator_params):
        KneeLocator_params_default = {"curve":'convex',
                                      "direction":'decreasing',
                                      "S":5}
        KneeLocator_params_default.update(KneeLocator_params)
        sse_avg = communities_descriptions.groupby("resolution").mean()["SSE"]
        x = sse_avg.index
        y = sse_avg
        kn = KneeLocator(x, y, **KneeLocator_params_default)
        return kn


    def make_tissue_repport(self,tissue,gsea_G,GSEA_GO_G,folder,X,tissues,tfs):
        tissue_folder = os.path.join(folder,tissue)
        tfs_description = {"TFs":[],"community":[]}
        if not os.path.exists(tissue_folder):
            os.mkdir(tissue_folder)
        if tissue in gsea_G.nodes():
            g = nx.ego_graph(gsea_G,tissue)
            plt.figure()
            self.plot_go_goas_network(g,prog="neato",GSEAs_nodes_size=12,communities_nodes_size=9)
            plt.savefig(os.path.join(tissue_folder,"gsea.pdf"))
            plt.clf()

            plt.figure()
            gsea_go_ego_tissue = nx.ego_graph(GSEA_GO_G,tissue,2)
            for t in list(set(tissues).difference(set([tissue]))):
                if t in gsea_go_ego_tissue.nodes:
                    gsea_go_ego_tissue.remove_node(t)
            self.plot_go_goas_network(gsea_go_ego_tissue,prog="neato",
                                        communities_color="navajowhite",
                                        GOs_color="lightsteelblue",
                                        GSEAs_color="indianred",
                                        communities_nodes_size=7,
                                        GOs_nodes_size=5,
                                        GSEAs_nodes_size=8,
                                        node_size_scale=30)
            plt.savefig(os.path.join(tissue_folder,"go_gsea.pdf"))
            plt.clf()

            for community in g[tissue]:
                if g[tissue][community]["nes"]>0:
                    c = int(community.split("|$")[1])
                    plt.figure()
                    self.community_heatmap_average_per_tissue(X,tissues,c,annot=False)
                    plt.savefig(os.path.join(tissue_folder,community+"_heatmap.pdf"))
                    plt.clf()

                    plt.figure()
                    self.plot_gsea_curve(tissue, c)
                    plt.savefig(os.path.join(tissue_folder,community+"_gsea.pdf"))
                    plt.clf()

                    #plt.figure()
                    #self.plot_community(c,threshold=0.0,labels=False)
                    #plt.savefig(os.path.join(tissue_folder,community+"_grn.pdf"))
                    #plt.clf()

                    tfs_com = self.communities[c].intersection(tfs)
                    tfs_description["TFs"]+=tfs_com
                    tfs_description["community"]+=[c for tf in tfs_com]

            tfs_description = pd.DataFrame(tfs_description)
            avg_profile = []
            for i,tf in enumerate(tfs_description["TFs"]):
                avg_profile.append(X[tf].groupby(tissues).mean()[tissue])
            tfs_description["avg expression"] = avg_profile
            tfs_description = tfs_description.sort_values("avg expression",ascending=False).reset_index()
            tfs_description.to_csv(os.path.join(tissue_folder,"TFs.csv"))

class GXN_OMP(__General_GXN__):
    def __init__(self,nb_features):
        params_OMPcv = {"fit_intercept":[False],
                       "normalize":[False],
                       "n_jobs":[1],
                       'max_iter':[nb_features],
                       'cv':[KFold(n_splits=5, shuffle=True, random_state=666)]}
        __General_GXN__.__init__(self,
                                 OrthogonalMatchingPursuitCV(normalize=False),
                                 **params_OMPcv)
    def feature_importance_function(self,predictor):
        '''
        Compute and return feature importance of inner predictor

        Returns:
            numpy.array: importance scores for each feature

        '''
        return predictor.coef_

class GXN_EN(__General_GXN__):
    def __init__(self,eps):
        params_ENcv = {"fit_intercept":[False],
                       "l1_ratio":[[0.8,0.9,0.99,1]],
                       "selection":["random"],
                       "tol":[1e-2],
                       "eps":[eps],
                       "n_alphas":[int(1./eps)],
                       "n_jobs":[1],
                       'cv':[KFold(n_splits=5, shuffle=True, random_state=33)]}

        __General_GXN__.__init__(self,
                                 ElasticNetCV(),
                                 **params_ENcv)
    def feature_importance_function(self,predictor):
        '''
        Compute and return feature importance of inner predictor

        Returns:
            numpy.array: importance scores for each feature

        '''
        return predictor.coef_
