from rdkit import Chem
from rdkit.Chem import Draw
import requests
from rdkit import Chem
from rdkit.Chem import MACCSkeys
from rdkit.Chem import AllChem
from rdkit.Chem import rdmolops
from base64 import b64decode
from rdkit import DataStructs
from rdkit.Chem import MACCSkeys
from rdkit.Chem import rdmolops
from  pybase64  import b64decode
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
from IPython.display import display
import requests
from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem import AllChem
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit import Chem
from rdkit.Chem import MCS
from rdkit import DataStructs



def PCFP_BitString(pcfp_base64) :

    pcfp_bitstring = "".join( ["{:08b}".format(x) for x in b64decode( pcfp_base64 )] )[32:913]
    return pcfp_bitstring

from rdkit import Chem

def bioactiveity_active__inactive_smliarity(e):
    ########################################find description link sids #####################################################
    sc=[]
    print("This code find active and inactive substance for given assay they it measure the smilarity between these inactive and active substance")

    description= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+"/description/xml"
    print("Here is link descript your entery assay ")
    print("")
    print(description)
    print("")
    #print("Here is list of substances are active in your assay ")
    print("")
    ########################################find active sids #####################################################

    active= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/sids/txt?sids_type=active"
    url=requests.get(active)
    cidactive= (url.text.split())
    #print(cids)
    ########################################find inactive sids #####################################################
    inactive= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/sids/txt?sids_type=inactive"
    url=requests.get(inactive)
    cidinactive= (url.text.split())
    ########################################find active Fingerprint2D #####################################################
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    str_cid = ",".join([ str(x) for x in cidactive])
    url = prolog + "/compound/cid/" + str_cid + "/property/Fingerprint2D/txt"
    res = requests.get(url)
    Fingerprint2Dactive = res.text.split()
    ########################################find inactive Fingerprint2D #####################################################
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    str_cid = ",".join([ str(x) for x in cidinactive])
    url = prolog + "/compound/cid/" + str_cid + "/property/Fingerprint2D/txt"
    res = requests.get(url)
    Fingerprint2Dinactive = res.text.split()
    ########################################find inactive & active snilarity score #####################################################

    for i in range(len(Fingerprint2Dactive)):
            for j in range(len(Fingerprint2Dinactive)) :
                fps1=(DataStructs.CreateFromBitString(PCFP_BitString(Fingerprint2Dactive[i])))
                fps2=(DataStructs.CreateFromBitString(PCFP_BitString(Fingerprint2Dinactive[j])))
                score = DataStructs.FingerprintSimilarity(fps1, fps2)
                print("active cid", cidactive[i], "vs.", "inactive", cidinactive[j], ":", round(score,3), end='')
                sc.append(str(score))
                    ########################################draw active structure #####################################################
                print("")

                print("Active molecule structure")
                print("")
                w1="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+ cidactive[i] +"/property/isomericsmiles/txt"
                res1 = requests.get(w1)
                img1 = Chem.Draw.MolToImage( Chem.MolFromSmiles( res1.text.rstrip() ), size=(200, 100)) 
                display(img1)

    ########################################draw inactive structure #####################################################
                print("Inactive molecule structure")
                print("")
                w2="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+ cidinactive[j] +"/property/isomericsmiles/txt"
                res2 = requests.get(w2)
                
                img2 = Chem.Draw.MolToImage( Chem.MolFromSmiles( res2.text.rstrip() ), size=(200, 100) )
                display(img2)
    ########################################print inactive & active snilarity score #####################################################

                if ( score >= 0.85 ):
                    print(" ****")
                elif ( score >= 0.75 ):
                    print(" ***")
                elif ( score >= 0.65 ):
                    print(" **")
                elif ( score >= 0.55 ):
                    print(" *")
                else:
                    print(" ")
    return
#bioactiveity_active__inactive_smliarity(1000)
import rdkit.Chem
import rdkit.Chem
from rdkit.Chem import MCS

    ########################################find description link sids #####################################################
def find_active_sids_for_aid(e):

    study= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(1000)+ "/sids/txt?sids_type=active"
    url=requests.get(study)
    cids= (url.text.split())
        #print(cidactive)
    str_cid = ",".join([ str(x) for x in cids])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    str_cid = ",".join([ str(x) for x in cids])

    url = prolog + "/compound/cid/" + str_cid + "/property/isomericsmiles/txt"
    res = requests.get(url)
    ms = res.text.split()
        #print(smiles)
        ########################################find active sids #####################################################

    ms = res.text.split()
    ms = list(map(rdkit.Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(ms, subImgSize=(400,400))
    r = MCS.FindMCS(ms, threshold=0.5)
    display(i)
    #rdkit.Chem.Draw.MolToImage(r.queryMol, size=(400,400))
    res = MCS.FindMCS(ms, threshold=0.7)
    ii= Chem.MolFromSmarts(res.smarts)
    Chem.MolFromSmarts(res.smarts)
    display(ii)
    return
#find_active_sids_for_aid(180)
import rdkit.Chem
import rdkit.Chem
from rdkit.Chem import MCS

    ########################################find description link sids #####################################################
def find_inactive_sids_for_aid(e):

    study= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(1000)+ "/sids/txt?sids_type=inactive"
    url=requests.get(study)
    cids= (url.text.split())
        #print(cidactive)
    str_cid = ",".join([ str(x) for x in cids])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    str_cid = ",".join([ str(x) for x in cids])

    url = prolog + "/compound/cid/" + str_cid + "/property/isomericsmiles/txt"
    res = requests.get(url)
    ms = res.text.split()
        #print(smiles)
        ########################################find active sids #####################################################

    ms = res.text.split()
    ms = list(map(rdkit.Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(ms, subImgSize=(400,400))
    r = MCS.FindMCS(ms, threshold=0.5)
    display(i)
    #rdkit.Chem.Draw.MolToImage(r.queryMol, size=(400,400))
    res = MCS.FindMCS(ms, threshold=0.7)
    ii= Chem.MolFromSmarts(res.smarts)
    Chem.MolFromSmarts(res.smarts)
    display(ii)
    return
#find_active_sids_for_aid(180)#find_active_sids_for_aid(100)
def assay_aid_sid_active_common_substracture(e):
    e=str(e)
    active= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=active"
    url=requests.get(active)
    cidactive= (url.text.split())

    print("These substance sids are \n \n", cidactive)
    str_cid = ",".join([ str(x) for x in cidactive])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    res = requests.get(url)
    ms = res.text.split()
        #print(smiles)
        ########################################find active sids #####################################################
    s = list(map(Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(s, subImgSize=(400,400))
    r = MCS.FindMCS(s, threshold=0.5)
    m= display(i)
    print("The common substracture with threshold=0.5 \n \n")
    res = MCS.FindMCS(s, threshold=0.5)
    i= Chem.MolFromSmarts(res.smarts)
    n= display(i)
    l=[]
    print( "The cilral center for these cid substancea are \n \n ")
    for i in range(len(s)):
        print(cidactive[i])
        print("")
        #print(i.GetNumAtoms())
        x= Chem.FindMolChiralCenters(s[i],force=True)
        print(x) 
        l.append(str(s[i].GetNumAtoms()))

    res = [eval(i) for i in l]
    print("")
    print("Average molecular weight for these compound is \n \n " ,sum(res)/len(res))

    return m,n
#assay_aid_sid_active_common_substracture(1000)

def assay_aid_sid_inactive_common_substracture(e):
    e=str(e)
    active= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=inactive"
    url=requests.get(active)
    cidactive= (url.text.split())

    print("These substance sids are \n \n", cidactive)
    str_cid = ",".join([ str(x) for x in cidactive])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    res = requests.get(url)
    ms = res.text.split()
        #print(smiles)
        ########################################find active sids #####################################################
    s = list(map(Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(s, subImgSize=(400,400))
    r = MCS.FindMCS(s, threshold=0.5)
    m= display(i)
    print("The common substracture threshold=0.5 \n \n")

    res = MCS.FindMCS(s, threshold=0.5)
    i= Chem.MolFromSmarts(res.smarts)
    n= display(i)
    l=[]
    print( "The cilral center for these cid substancea are  \n \n ")
    for i in range(len(s)):
        print(cidactive[i])
        print("")
        #print(i.GetNumAtoms())
        x= Chem.FindMolChiralCenters(s[i],force=True)
        print(x) 
        l.append(str(s[i].GetNumAtoms()))

    res = [eval(i) for i in l]
    print("")
    print("Average molecular weight for these compound is \n \n " ,sum(res)/len(res))
    return m,n
#assay_aid_sid_inactive_common_substracture(1000)

def compound_smile_to_morgan_atom_topological(a,b): 
    ms = [Chem.MolFromSmiles(a), Chem.MolFromSmiles(b)]
    fig=Draw.MolsToGridImage(ms[:],molsPerRow=2,subImgSize=(400,200))
    display(fig)
    from rdkit.Chem.AtomPairs import Pairs
    from rdkit.Chem import AllChem
    from rdkit.Chem.Fingerprints import FingerprintMols
    from rdkit import DataStructs

    radius = 2

    fpatom = [Pairs.GetAtomPairFingerprintAsBitVect(x) for x in ms]
    fpatom = [Pairs.GetAtomPairFingerprintAsBitVect(x) for x in ms]

    print("atom pair score: {:8.4f}".format(DataStructs.TanimotoSimilarity(fpatom[0], fpatom[1])))
    fpmorg = [AllChem.GetMorganFingerprint(ms[0],radius,useFeatures=True),
              AllChem.GetMorganFingerprint(ms[1],radius,useFeatures=True)]
    fptopo = [FingerprintMols.FingerprintMol(x) for x in ms]
    print("morgan score: {:11.4f}".format(DataStructs.TanimotoSimilarity(fpmorg[0], fpmorg[1])))
    print("topological score: {:3.4f}".format(DataStructs.TanimotoSimilarity(fptopo[0], fptopo[1])))
    return
#compound_smile_to_morgan_atom_topological("CCO","CNCN")