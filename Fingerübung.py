import os
import xml.etree.ElementTree as ET
from spacy.lang.en import English
import spacy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
##############################################################################
#read in text from xml files
#Task 2.2
def read_in(path):
    text_list = []
    path = os.path.abspath(path)
    for filename in os.listdir(path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(path, filename)
        tree = ET.parse(fullname)
        root = tree.getroot()
        for rank in (root.iter('TEXT')):
            #rank.text ist mein text aus der xml
            text_list.append(rank.text)
    
    return text_list
##############################################################################
#tokening
#Task 2.2
def tokening(text):
    nlp = English()
    doc = nlp(text)
    for token in doc:
        print(token.text)
        
##############################################################################
#Part of speech tags
#Task 2.2
def token_and_tag(text):
    nlp = English()
    doc = nlp(text)
    
    #load the small english model
    nlp = spacy.load("en_core_web_sm")
    #Process text
    doc = nlp(text)
    #Iterate over token
    result = []
    for token in doc:
        result.append([token.text, token.pos_])
    return result   
##############################################################################
#Evaluate information about PoS Tags
#Task 2.3.1
#print(list_ANC_Japan[0][0] + ' has ' + str( pos_counting(list_ANC_Japan[0][1])))
def pos_counting(tagged_elements):
    tag_dicc = {}
    for j in range(0,len(tagged_elements)):
        for element in tagged_elements[j]:
            pos_tag = element[1]    #list with PoS Tags
            #go through every element in text list
            if pos_tag not in tag_dicc:
                tag_dicc[pos_tag] = 1
            else:
                tag_dicc[pos_tag] += 1
        
    return(tag_dicc)
##############################################################################
#liest den teil tags ein von der xml
def read_tags(path):
    tags_list = []
    
    path = os.path.abspath(path)
    for filename in os.listdir(path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(path, filename)
        position_list = []
        my_file = open(fullname, "r", encoding = 'utf-8', errors = 'ignore')
        lines_of_file = my_file.readlines()
        for c,i in enumerate(lines_of_file):
            if 'TAGS' in i:
                position_list.append(c)
        
        tags = (lines_of_file[position_list[0]:position_list[1]+1])
        tags_list.append(tags)
    return tags_list
##############################################################################
#Task 2.3.2
def count_iso_types(tags_list):
    
    places = 0
    spatial_entity = 0
    motion = 0
    signal = 0
    qslink = 0
    olink = 0
    for tag in tags_list:
       for text in tag:
           
           if (text[1:6]) == "PLACE":
               places += 1
           if (text[1:15]) == "SPATIAL_ENTITY":
               spatial_entity += 1
           if (text[1:7]) == "MOTION":
               motion += 1
           if (text[1:15]) == "SPATIAL_SIGNAL" or ((text[1:14]) == "MOTION_SIGNAL"):
               signal += 1
           if(text[1:7] == "QSLINK"):
               qslink += 1
           if(text[1:6] == "OLINK"):
               olink += 1
    result = [["places:" , places], ["spatialentity" , spatial_entity] ,
              ["motions:" , motion],["signal", signal],["qslinks:", qslink],["olinks" , olink]]
             
    return result
##############################################################################
def qsrelations():
    tags_list = main_read_tags()
    dicc_of_qs = {}
    for tag in tags_list:
       for text in tag:
           if(text[1:7] == "QSLINK"):
              spaced_text = (text.replace("=", " "))
              splitted_text = spaced_text.split()
              #print(splitted_text)
              for i in splitted_text:
                  if i == "relType":
                      reltype_index = (splitted_text.index(i))
                      qsrel = (splitted_text[reltype_index +1])
                       
                      if qsrel not in dicc_of_qs:
                          dicc_of_qs[qsrel] = 1
                      else:
                          dicc_of_qs[qsrel] += 1
    return dicc_of_qs
##############################################################################
def sentence_length():
    sntc_lngth_dicc = {}
    text_list = main_readin()
    for i in range(0, len(text_list)):
        replaced_text = (text_list[i].replace("." , " XXXENDOFSENTENCEXXX "))
        splitted_text = replaced_text.split()
        sntc_lngth = 0
        for i in splitted_text:
            if i == "XXXENDOFSENTENCEXXX":
                if sntc_lngth not in sntc_lngth_dicc:
                    sntc_lngth_dicc[sntc_lngth] = 1
                else:
                    sntc_lngth_dicc[sntc_lngth] += 1
                sntc_lngth = 0
            else:
                sntc_lngth += 1
        
    return(sntc_lngth_dicc)
##############################################################################
def spatial_triggers():
    tags_list = main_read_tags()
    trigger_dicc_qs = {}
    trigger_dicc_os = {}
    for tag in tags_list:
       id_text_signal = []
       trigger_qs = []
       trigger_os = []     
       for text in tag:
           if (text[1:15]) == "SPATIAL_SIGNAL" :
               spatial_text = (text.replace("=", " ").split())
               id_and_text = []                            
               for i in range(0,len(spatial_text)):                                      
                   if(spatial_text[i] == "id"):                       
                       id_and_text.append(spatial_text[i+1])           
                   if(spatial_text[i] == "text"):
                       id_and_text.append(spatial_text[i+1])
               id_text_signal.append(id_and_text)
           
           if(text[1:7] == "QSLINK"):
               qs_text = (text.replace("="," ").split())
               for i in range(0,len(qs_text)):
                   if(qs_text[i] == "trigger"):
                       trigger_qs.append(qs_text[i+1])
                       
           if(text[1:6] == "OLINK"):
               os_text = (text.replace("="," ").split())
               for i in range(0,len(os_text)):
                   if(os_text[i] == "trigger"):
                       trigger_os.append(os_text[i+1])
       for id_text in id_text_signal:
           id = id_text[0]
           text = id_text[1]
           if id in trigger_qs:
               if text not in trigger_dicc_qs:
                   trigger_dicc_qs[text] = 1
               else:
                   trigger_dicc_qs[text] += 1
           if id in trigger_os:
               if text not in trigger_dicc_os:
                   trigger_dicc_os[text] = 1
               else:
                   trigger_dicc_os[text] += 1
    print("\n qs was triggered by: \n " , trigger_dicc_qs)
    print("\n os was triggered by: \n ", trigger_dicc_os)
##############################################################################
def movement_verbs():
    move_dicc = {}
    master_list = main_read_tags()
    for tag in master_list:
        for text in tag:
            if (text[1:9]) == "MOVELINK":
                move_text = text.replace("=", " ").split()
                for i in range(0, len(move_text)):
                    if move_text[i] == "fromText":
                        if(move_text[i+1]) not in move_dicc:
                            move_dicc[move_text[i+1]] = 1
                        else:
                            move_dicc[move_text[i+1]] += 1
    counter = 1
    while (counter!=6):
        verb = (max(move_dicc)[1:len(max(move_dicc))-1])
        if (isVerb(verb)):
            print("Number " , counter , "of most used movement verbs is: ", verb)
            counter +=1
            del move_dicc[max(move_dicc)]
        else:
            del move_dicc[max(move_dicc)]
##############################################################################
def isVerb(word):
    #load the small english model
    nlp = spacy.load("en_core_web_sm")
    #Process text
    doc = nlp(word)
    #Iterate over token
    result = []
    for token in doc:
        result.append([token.text, token.pos_])  
    if (result[0][1])== "VERB":
        return True
    else:
        return False
##############################################################################
def graph_x_y():
    # Data for plotting  
    xcoord = []
    ycoord = []
    print(sentence_length())
    data = sentence_length()
    for i in (data):
        xcoord.append(i)
        ycoord.append(data[i])

    fig , ax = plt.subplots()
    ax.plot(xcoord, ycoord,'ro')
    print("\n The graph was Saved as 234.png")
    fig.savefig("234.png")
    plt.show()    
##############################################################################    
def read_bicycles_tags(path):
    tags_list = []
    
    path = os.path.abspath(path)
    for filename in os.listdir(path):
        if (filename != "Bicycles.xml"):continue
        if (not filename.endswith('.xml')) : continue    
        fullname = os.path.join(path, filename)
        position_list = []
        my_file = open(fullname, "r", encoding = 'utf-8', errors = 'ignore')
        lines_of_file = my_file.readlines()
        for c,i in enumerate(lines_of_file):
            if 'TAGS' in i:
                position_list.append(c)
        
        tags = (lines_of_file[position_list[0]:position_list[1]+1])
        tags_list.append(tags)
    return(tags_list[0])
############################################################################## 
def read_prado_tags(path):
    tags_list = []
    
    path = os.path.abspath(path)
    for filename in os.listdir(path):
        if (filename != "Highlights_of_the_Prado_Museum.xml"):continue
        if (not filename.endswith('.xml')) : continue    
        fullname = os.path.join(path, filename)
        position_list = []
        my_file = open(fullname, "r", encoding = 'utf-8', errors = 'ignore')
        lines_of_file = my_file.readlines()
        for c,i in enumerate(lines_of_file):
            if 'TAGS' in i:
                position_list.append(c)
        
        tags = (lines_of_file[position_list[0]:position_list[1]+1])
        tags_list.append(tags)
    return(tags_list[0])
##############################################################################
def get_nodes(tags):
    place_nodes = []
    spatial_entity_nodes = []
    master_nodes = []
    for text in tags:
        node = []
        if (text[1:6] ) == "PLACE":
            place_text = text.replace("=", " ").split()
            for i in range(0,len(place_text)):
                if(place_text[i] == "text"):
                    node.append(place_text[i+1])
                if(place_text[i] == "id"):
                    node.append(place_text[i+1])
            place_nodes.append(node)
        if (text[1:15]) == "SPATIAL_ENTITY":
            spatial_text = text.replace("=", " ").split()
            for i in range(0,len(spatial_text)):
                if(spatial_text[i] == "text"):
                    node.append(spatial_text[i+1])
                if(spatial_text[i] == "id"):
                    node.append(spatial_text[i+1])
            spatial_entity_nodes.append(node)
    master_nodes = [place_nodes, spatial_entity_nodes]
    #REMOVE NODES THROUGH METALINK INFORMATION
    master_nodes = metalink_check(tags,master_nodes)
    return master_nodes
##############################################################################   
def metalink_check(tags, master_nodes):
    place_nodes = master_nodes[0]
    spatial_entity_nodes = master_nodes[1]
    metalink = []
    #GET METALINK INFORMATION
    for text in tags:
        metalink_info = []
        if (text[1:9]) == "METALINK" :
            metalink_text = text.replace("=", " ").split()
            for i in range(0,len(metalink_text)):
                if metalink_text[i] == "toText":
                    metalink_info.append(metalink_text[i+1])
                if metalink_text[i] == "toID":
                    metalink_info.append(metalink_text[i+1])
                if metalink_text[i] == "fromID":
                    metalink_info.append(metalink_text[i+1])
            metalink.append(metalink_info)
        
    #Remove nodes through metalink information
    #Place nodes removal
    for metainfo in metalink:
        fromID = metainfo[0]
        for node in place_nodes:
            if (node[0]) == fromID :
                place_nodes.remove(node)
    
    #Spatial entity nodes removal
    for metainfo in metalink:
        fromID = metainfo[0]
        for node in spatial_entity_nodes:
            if(node[0]) == fromID :
                spatial_entity_nodes.remove(node)
    return ([place_nodes, spatial_entity_nodes])
##############################################################################
def get_edges(tags):
    qs_edges = []
    os_edges = []
    for text in tags:
        edge = []
        if(text[1:7] == "QSLINK"):
            qs_text = text.replace("=", " ").split()
            for i in range (0,len(qs_text)):                
                if qs_text[i] == ("fromText") :
                    edge.append(qs_text[i+1])
                if qs_text[i] == ("toText"):
                    edge.append(qs_text[i+1])
                if qs_text[i] == ("relType"):
                    edge.append(qs_text[i+1])
            qs_edges.append(edge)
        if(text[1:6] == "OLINK"):
            os_text = text.replace("=", " ").split()                  
            for i in range (0,len(os_text)):                
                if os_text[i] == ("fromText") :
                    edge.append(os_text[i+1])
                if os_text[i] == ("toText"):
                    edge.append(os_text[i+1])
                if os_text[i] == ("relType"):
                    edge.append(os_text[i+1])
            os_edges.append(edge)
    
    master_edges = [qs_edges , os_edges]       
    return master_edges
##############################################################################
def generate_graph(nodes, edges, saveAs):
    place_nodes = nodes[0]
    spatial_entity_nodes = nodes[1]
    qs_edges = edges[0]
    os_edges = edges[1]
    print("\n nodes for: " , saveAs , "are: \n", nodes)
    print("\n edges for: " , saveAs , "are: \n", edges)
    G = nx.DiGraph()
    #Add nodes
    counter_x = 1
    counter_y = 1
    for node in place_nodes:
        G.add_node(node[1] , typeof = "place")

    for node in spatial_entity_nodes:
        G.add_node(node[1], typeof = "spatial")

    #Color nodes
    color_map = nx.get_node_attributes(G, "typeof")
    for key in color_map:
        if color_map[key] == "place":
            color_map[key] = "red"
        else:
            color_map[key] = "blue"
    
    colors_for_nodes = [color_map.get(node) for node in G.nodes()]
    #Add edges    
    for edges in qs_edges:        
        u = edges[0]
        v = edges[1]
        if u in G.nodes():
            if v in G.nodes():
                G.add_edge(u,v , typeof = "qs")
                
        
    for edges in os_edges:
        u = edges[0]
        v = edges[1]
        if u in G.nodes():
            if v in G.nodes():
                G.add_edge(u,v, typeof = "os")
    
    #Labeling edges :
    edge_labels = {}  
    for edges in qs_edges:
        u = edges[0]
        v = edges[1]
        label = edges[2]
        key = (u,v)    
        edge_labels[key] = label

    pos = nx.spring_layout(G)
    plt.figure()    
    
    nx.draw(G, pos,with_labels=True , node_color = colors_for_nodes )
    nx.draw_networkx_edge_labels(G,pos, edge_label = edge_labels)
    plt.savefig(saveAs)
    plt.show() 
    print("\n Saved as:" , saveAs + "\n")

##############################################################################
def main_readin():
    list_ANC_Japan = (read_in("TrainingData2\Traning\ANC\WhereToJapan"))
    list_ANC_Madrid = (read_in("TrainingData2\Traning\ANC\WhereToMadrid"))
    list_CP = (read_in("TrainingData2\Traning\CP"))
    list_RFC = (read_in("TrainingData2\Traning\RFC"))
    master_list = list_ANC_Japan + list_ANC_Madrid + list_CP + list_RFC
    return master_list
##############################################################################
def main_tag(master_list): 
    for i in range(0,len(master_list)):
        master_list[i] = token_and_tag(master_list[i])
    return master_list
##############################################################################
def main_231(master_list):
    master_list = main_tag(master_list)
    print( pos_counting(master_list))
##############################################################################
def main_read_tags():
    list_ANC_Japan = (read_tags("TrainingData2\Traning\ANC\WhereToJapan"))
    list_ANC_Madrid = (read_tags("TrainingData2\Traning\ANC\WhereToMadrid"))
    list_CP = (read_tags("TrainingData2\Traning\CP"))
    list_RFC = (read_tags("TrainingData2\Traning\RFC"))
    master_list = list_ANC_Japan + list_ANC_Madrid + list_CP + list_RFC
    return master_list
##############################################################################
def main_232():
    master_list = main_read_tags()
    print(count_iso_types(master_list))
    
##############################################################################
def main_24():
    #Create graph for bycicles.xml
    bycicles_tags = read_bicycles_tags("TrainingData2\Traning\RFC")
    bycicle_nodes = get_nodes(bycicles_tags)
    bycicle_edges = get_edges(bycicles_tags)
    generate_graph(bycicle_nodes, bycicle_edges, "bicyclesGraph.png")
    #create graph for prado.xml
    prado_tags = read_prado_tags("TrainingData2\Traning\ANC\WhereToMadrid")
    prado_nodes  = get_nodes(prado_tags)
    prado_edges = get_edges(prado_tags)
    generate_graph(prado_nodes, prado_edges , "pradoGraph.png")
##############################################################################
def main():
    inpt = 0
    while (inpt != "9"):
        
        print("_______________________________________________________________________________________")
        print("\n")
        print("Enter 1 for task 2.2 - Read in xml ")
        print("Enter 2 for task 2.3.1 - Counted PoS Tags")
        print("Enter 3 for task 2.3.2 - Counting of Tags")
        print("Enter 4 for task 2.3.3 - QS Types")
        print("Enter 5 for task 2.3.4 - Sentence length + Visual representation : In 234.png")
        print("Enter 6 for task 2.3.5 - Spatial triggers")
        print("Enter 7 for task 2.3.6 - Most used movement verbs")
        print("Enter 8 for task 2.4 - Graph of bicycles and Prado Museum")
        print("Enter 9 to finish")
        inpt = input("Please enter the number: ")
        
        
        if (inpt == "1"):
            #TASK 2.2
            #[text,text...]
            print("_______________________________________________________________________________________")
            print("Please wait!")
            master_list = main_readin()
            print("\n Read in of all texts: \n")
            print(master_list)
            print("\n")
            #___________________________________________________________________________
            #pos tags
            #Taggen und Token
            #[[[a,b],[a,b]...]...]
            print("Token and PoS Tags: \n")
            print((main_tag(master_list)))
            
        #2.3.1
        #dictionary with counted PoS Tag values
        if (inpt == "2"):   
            print("_______________________________________________________________________________________")
            print("\n Task 2.3.1 Counted PoS Tags!  Please wait! \n")
            master_list = main_readin()
            main_231(master_list)
        
        #2.3.2
        if (inpt == "3"):
            print("_______________________________________________________________________________________")
            print("\n Task 2.3.2 - Qs Types : \n")
            if(inpt == "3"):
                (main_232())
        
        
        #2.3.3 qs relations 
        if (inpt == "4"):
            print("_______________________________________________________________________________________")
            print("\n Task 2.3.3 - Qs Types \n")
            print (qsrelations())
        
        #2.3.4
        if (inpt == "5"):
            print("_______________________________________________________________________________________")
            print("\n Sentence lengths : \n")    
            graph_x_y()
        #2.3.5
        if (inpt == "6"): 
            print("_______________________________________________________________________________________")
            print("\n Task 2.3.5 - QS/OS spatial triggers \n")
            spatial_triggers()
        
        #2.3.6
        if (inpt == "7"):
            print("_______________________________________________________________________________________")
            print("\n Task 2.3.6 - Most used movement verbs: \n")
            movement_verbs()
        
        
        if (inpt == "8"):
            print("_______________________________________________________________________________________")
            print("\n Task 2.4 Graph ")
            main_24()

main()
