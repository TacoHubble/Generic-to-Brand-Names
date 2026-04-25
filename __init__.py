# __init__.py v1.6.1 — Fixed ImportError & Consolidated Library
from __future__ import annotations
from aqt import mw
from aqt.gui_hooks import card_will_show
from aqt.utils import showWarning, qconnect
from aqt.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QDialogButtonBox, QInputDialog, QMessageBox, QCheckBox
)
import re

ADDON_NAME = "Generic to Brand Names"

DEFAULT_CFG = {
    "only_if_deck_startswith": [],
    "only_if_note_has_any_tag": [],
    "case_sensitive": False,
    "delimiter": "; ",
    "insert_format": " {brandparen}",
    "extra_map": {},
    "debug_flag": "",
    "exclude_terms": [],
    "exclude_decks": [],
    "exclude_tags": []
}

def _get_cfg():
    cfg = mw.addonManager.getConfig(__name__) or {}
    for k, v in DEFAULT_CFG.items():
        cfg.setdefault(k, v)
    return cfg

def _save_cfg(cfg):
    mw.addonManager.writeConfig(__name__, cfg)

# ---- Default Library ----
LIBRARY_MAP = {
    "abaloparatide": ["Tymlos"],
    "abatacept": ["Orencia"],
    "abciximab": ["ReoPro"],
    "acebutolol": ["Sectral"],
    "acetaminophen": ["Tylenol"],
    "acetaminophen-codeine": ["Tylenol #3"],
    "acetaminophen-hydrocodone": ["Norco", "Vicodin", "Lortab"],
    "acetylcysteine": ["Mucomyst", "Acetadote"],
    "acyclovir": ["Zovirax"],
    "adalimumab": ["Humira"],
    "albuterol": ["Ventolin", "ProAir", "Proventil"],
    "alemtuzumab": ["Campath", "Lemtrada"],
    "alendronate": ["Fosamax"],
    "alfuzosin": ["Uroxatral"],
    "alirocumab": ["Praluent"],
    "allopurinol": ["Zyloprim", "Aloprim"],
    "alogliptin": ["Nesina"],
    "alprazolam": ["Xanax"],
    "alteplase": ["Activase", "Cathflo"],
    "amantadine": ["Gocovri", "Osmolex ER", "Symmetrel"],
    "amiloride": ["Midamor"],
    "amiodarone": ["Pacerone", "Cordarone"],
    "amitriptyline": ["Elavil"],
    "amlodipine": ["Norvasc"],
    "amoxicillin": ["Amoxil"],
    "amoxicillin-clavulanate": ["Augmentin"],
    "amphetamine-dextroamphetamine": ["Adderall", "Adderall XR", "Mydayis"],
    "amphotericin b": ["Fungizone", "Ambisome"],
    "ampicillin": ["Principen"],
    "ampicillin-sulbactam": ["Unasyn"],
    "anastrozole": ["Arimidex"],
    "apixaban": ["Eliquis"],
    "aprepitant": ["Emend"],
    "aripiprazole": ["Abilify"],
    "armodafinil": ["Nuvigil"],
    "articaine": ["Septocaine"],
    "asenapine": ["Saphris"],
    "aspirin": ["Bayer", "Ecotrin"],
    "atazanavir": ["Reyataz"],
    "atenolol": ["Tenormin"],
    "atogepant": ["Qulipta"],
    "atomoxetine": ["Strattera"],
    "atorvastatin": ["Lipitor"],
    "atracurium": ["Tracrium"],
    "avanafil": ["Stendra"],
    "avelumab": ["Bavencio"],
    "azathioprine": ["Imuran"],
    "azelastine": ["Astelin", "Astepro"],
    "azilsartan": ["Edarbi"],
    "azithromycin": ["Zithromax", "Z-Pak"],
    "basiliximab": ["Simulect"],
    "beclomethasone": ["Qvar"],
    "bempedoic acid": ["Nexletol"],
    "benazepril": ["Lotensin"],
    "benralizumab": ["Fasenra"],
    "benznidazole": ["Lampit"],
    "benzocaine": ["Anbesol", "Orajel"],
    "benztropine": ["Cogentin"],
    "betamethasone": ["Diprolene", "Celestone"],
    "betaxolol": ["Kerlone"],
    "bevacizumab": ["Avastin"],
    "bictegravir-emtricitabine-tenofovir alafenamide": ["Biktarvy"],
    "bimatoprost": ["Lumigan"],
    "bismuth subsalicylate": ["Pepto-Bismol"],
    "bisoprolol": ["Zebeta"],
    "brexpiprazole": ["Rexulti"],
    "brimonidine": ["Alphagan P"],
    "brivaracetam": ["Briviact"],
    "bromazepam": [],
    "budesonide": ["Pulmicort"],
    "budesonide-formoterol": ["Symbicort"],
    "bumetanide": ["Bumex"],
    "bupivacaine": ["Marcaine", "Sensorcaine"],
    "buprenorphine": ["Subutex", "Belbuca", "Butrans"],
    "buprenorphine-naloxone": ["Suboxone", "Zubsolv"],
    "bupropion": ["Wellbutrin", "Zyban"],
    "burosumab": ["Crysvita"],
    "buspirone": ["Buspar"],
    "calcitriol": ["Rocaltrol"],
    "canagliflozin": ["Invokana"],
    "candesartan": ["Atacand"],
    "captopril": ["Capoten"],
    "carbamazepine": ["Tegretol"],
    "carbenicillin": ["Geocillin"],
    "carbidopa": ["Lodosyn"],
    "carbidopa-levodopa": ["Sinemet"],
    "cariprazine": ["Vraylar"],
    "carteolol": ["Ocupress"],
    "carvedilol": ["Coreg"],
    "cefadroxil": ["Duricef"],
    "cefazolin": ["Ancef"],
    "cefdinir": ["Omnicef"],
    "cefepime": ["Maxipime"],
    "cefiderocol": ["Fetroja"],
    "cefoperazone": [],
    "cefotaxime": ["Claforan"],
    "ceftaroline": ["Teflaro"],
    "ceftazidime": ["Fortaz", "Tazicef"],
    "ceftolozane-tazobactam": ["Zerbaxa"],
    "ceftriaxone": ["Rocephin"],
    "cefuroxime": ["Ceftin"],
    "celecoxib": ["Celebrex"],
    "cenobamate": ["Xcopri"],
    "cephalexin": ["Keflex"],
    "cetirizine": ["Zyrtec"],
    "chlordiazepoxide": ["Librium"],
    "chlorpromazine": ["Thorazine"],
    "chlorthalidone": ["Hygroton", "Thalitone"],
    "cholestyramine": ["Questran"],
    "ciclesonide": ["Alvesco"],
    "cilostazol": ["Pletal"],
    "cinacalcet": ["Sensipar"],
    "ciprofloxacin": ["Cipro"],
    "cisatracurium": ["Nimbex"],
    "citalopram": ["Celexa"],
    "clarithromycin": ["Biaxin"],
    "clindamycin": ["Cleocin"],
    "clobetasol": ["Temovate"],
    "clonazepam": ["Klonopin"],
    "clonidine": ["Catapres"],
    "clopidogrel": ["Plavix"],
    "clozapine": ["Clozaril"],
    "codeine": [],
    "colchicine": ["Colcrys", "Mitigare"],
    "colesevelam": ["Welchol"],
    "colestipol": ["Colestid"],
    "cyclobenzaprine": ["Flexeril", "Amrix"],
    "cyclosporine": ["Neoral", "Gengraf", "Sandimmune"],
    "dabigatran": ["Pradaxa"],
    "dalbavancin": ["Dalvance"],
    "dalteparin": ["Fragmin"],
    "dapagliflozin": ["Farxiga"],
    "dapsone": ["Aczone"],
    "daptomycin": ["Cubicin"],
    "daridorexant": ["Quviviq"],
    "darifenacin": ["Enablex"],
    "darunavir": ["Prezista"],
    "delafloxacin": ["Baxdela"],
    "denosumab": ["Prolia", "Xgeva"],
    "desiccated thyroid": ["Armour Thyroid"],
    "desloratadine": ["Clarinex"],
    "desmopressin": ["DDAVP", "Noctiva", "Stimate"],
    "desvenlafaxine": ["Pristiq"],
    "dexlansoprazole": ["Dexilant"],
    "dexmedetomidine": ["Precedex"],
    "dextroamphetamine": ["Dexedrine"],
    "dextromethorphan": ["Delsym"],
    "dextromethorphan-bupropion": ["Auvelity"],
    "diazepam": ["Valium"],
    "diclofenac": ["Voltaren", "Cataflam"],
    "dicyclomine": ["Bentyl"],
    "diflunisal": ["Dolobid"],
    "digoxin": ["Lanoxin"],
    "digoxin immune fab": ["DigiFab", "Digibind"],
    "dihydroergotamine": ["Migranal", "DHE 45"],
    "diltiazem": ["Cardizem", "Tiazac"],
    "dimenhydrinate": ["Dramamine"],
    "diphenhydramine": ["Benadryl"],
    "diphenoxylate-atropine": ["Lomotil"],
    "dipyridamole": ["Persantine"],
    "disopyramide": ["Norpace"],
    "divalproex": ["Depakote"],
    "dofetilide": ["Tikosyn"],
    "dolutegravir": ["Tivicay"],
    "dorzolamide": ["Trusopt"],
    "doxazosin": ["Cardura"],
    "doxepin": ["Silenor"],
    "doxorubicin": ["Adriamycin", "Doxil"],
    "doxycycline": ["Vibramycin", "Doryx"],
    "dronedarone": ["Multaq"],
    "dulaglutide": ["Trulicity"],
    "duloxetine": ["Cymbalta"],
    "dutasteride": ["Avodart"],
    "edoxaban": ["Savaysa"],
    "efavirenz": ["Sustiva"],
    "eletriptan": ["Relpax"],
    "elotuzumab": ["Empliciti"],
    "empagliflozin": ["Jardiance"],
    "emtricitabine": ["Emtriva"],
    "emtricitabine-tenofovir alafenamide": ["Descovy"],
    "emtricitabine-tenofovir df": ["Truvada"],
    "enalapril": ["Vasotec"],
    "enoxaparin": ["Lovenox"],
    "entacapone": ["Comtan"],
    "epinephrine": ["EpiPen", "Auvi-Q", "Adrenaclick"],
    "eplerenone": ["Inspra"],
    "epoetin alfa": ["Epogen", "Procrit", "Retacrit"],
    "eptifibatide": ["Integrilin"],
    "eptinezumab": ["Vyepti"],
    "erenumab": ["Aimovig"],
    "erlotinib": ["Tarceva"],
    "ertapenem": ["Invanz"],
    "erythromycin": ["Ery-Tab", "E.E.S"],
    "escitalopram": ["Lexapro"],
    "esomeprazole": ["Nexium"],
    "eszopiclone": ["Lunesta"],
    "etanercept": ["Enbrel"],
    "ethambutol": ["Myambutol"],
    "ethosuximide": ["Zarontin"],
    "etodolac": ["Lodine"],
    "etonogestrel implant": ["Nexplanon"],
    "evolocumab": ["Repatha"],
    "exenatide": ["Byetta", "Bydureon"],
    "ezetimibe": ["Zetia"],
    "ezetimibe-simvastatin": ["Vytorin"],
    "famciclovir": ["Famvir"],
    "famotidine": ["Pepcid"],
    "felodipine": ["Plendil"],
    "fenofibrate": ["Tricor", "Antara"],
    "fentanyl": ["Duragesic", "Actiq"],
    "fesoterodine": ["Toviaz"],
    "fexofenadine": ["Allegra"],
    "fidaxomicin": ["Dificid"],
    "finasteride": ["Proscar", "Propecia"],
    "flecainide": ["Tambocor"],
    "fluconazole": ["Diflucan"],
    "flumazenil": ["Romazicon"],
    "flunisolide": ["Aerospan"],
    "fluorouracil": ["Adrucil", "Efudex"],
    "fluoxetine": ["Prozac"],
    "fluphenazine": ["Prolixin"],
    "fluticasone": ["Flovent", "Flonase"],
    "fluticasone-salmeterol": ["Advair"],
    "fluticasone-vilanterol": ["Breo Ellipta"],
    "fomepizole": ["Antizol"],
    "fondaparinux": ["Arixtra"],
    "formoterol": ["Perforomist"],
    "fosfomycin": ["Monurol"],
    "fremanezumab": ["Ajovy"],
    "frovatriptan": ["Frova"],
    "furosemide": ["Lasix"],
    "gabapentin": ["Neurontin"],
    "galcanezumab": ["Emgality"],
    "ganciclovir": ["Cytovene", "Zirgan"],
    "gatifloxacin (ophthalmic)": ["Zymaxid"],
    "glimepiride": ["Amaryl"],
    "glipizide": ["Glucotrol"],
    "glyburide": ["Diabeta", "Micronase"],
    "glycopyrrolate": ["Robinul"],
    "glycopyrrolate-formoterol": ["Bevespi Aerosphere"],
    "goserelin": ["Zoladex"],
    "granisetron": ["Kytril", "Sancuso"],
    "guaifenesin": ["Mucinex", "Robitussin"],
    "guanfacine": ["Intuniv", "Tenex"],
    "haloperidol": ["Haldol"],
    "hydralazine": ["Apresoline"],
    "hydrochlorothiazide": ["Microzide"],
    "hydrocodone": ["Hysingla ER"],
    "hydromorphone": ["Dilaudid"],
    "hydroxocobalamin": ["Cyanokit"],
    "hydroxychloroquine": ["Plaquenil"],
    "hydroxyurea": ["Hydrea", "Droxia", "Siklos"],
    "hydroxyzine": ["Vistaril", "Atarax"],
    "hyoscyamine": ["Levsin", "Anaspaz"],
    "ibandronate": ["Boniva"],
    "ibuprofen": ["Advil", "Motrin"],
    "icosapent ethyl": ["Vascepa"],
    "ifosfamide": ["Ifex"],
    "iloperidone": ["Fanapt"],
    "iloprost": ["Ventavis"],
    "imatinib": ["Gleevec"],
    "imipenem-cilastatin": ["Primaxin"],
    "imipramine": ["Tofranil"],
    "indacaterol": ["Arcapta Neohaler"],
    "indapamide": ["Lozol"],
    "indomethacin": ["Indocin"],
    "infliximab": ["Remicade"],
    "insulin aspart": ["Novolog", "Fiasp"],
    "insulin degludec": ["Tresiba"],
    "insulin detemir": ["Levemir"],
    "insulin glargine": ["Lantus", "Basaglar", "Toujeo"],
    "insulin glulisine": ["Apidra"],
    "insulin human inhalation": ["Afrezza"],
    "insulin lispro": ["Humalog", "Admelog"],
    "insulin nph": ["Humulin N", "Novolin N"],
    "insulin premixed 70/30": ["Humulin 70/30", "Novolin 70/30"],
    "insulin regular": ["Humulin R", "Novolin R"],
    "ipratropium": ["Atrovent"],
    "isocarboxazid": ["Marplan"],
    "isoniazid": ["Nydrazid"],
    "isosorbide": ["Isordil", "Dilatrate"],
    "isosorbide dinitrate": ["Isordil"],
    "isosorbide mononitrate": ["Imdur"],
    "isotretinoin": ["Accutane", "Claravis", "Absorica"],
    "isradipine": ["Dynacirc"],
    "itraconazole": ["Sporanox"],
    "ivabradine": ["Corlanor"],
    "ketamine": ["Ketalar"],
    "ketorolac": ["Toradol"],
    "ketotifen": ["Zaditor", "Alaway"],
    "labetalol": ["Trandate", "Normodyne"],
    "lacosamide": ["Vimpat"],
    "lactulose": ["Kristalose", "Enulose"],
    "lamivudine": ["Epivir"],
    "lamotrigine": ["Lamictal"],
    "lansoprazole": ["Prevacid"],
    "lasmiditan": ["Reyvow"],
    "latanoprost": ["Xalatan"],
    "leflunomide": ["Arava"],
    "lemborexant": ["Dayvigo"],
    "letrozole": ["Femara"],
    "leucovorin": ["Wellcovorin", "Folinic Acid"],
    "levalbuterol": ["Xopenex"],
    "levetiracetam": ["Keppra"],
    "levobunolol": ["Betagan"],
    "levocetirizine": ["Xyzal"],
    "levofloxacin": ["Levaquin"],
    "levonorgestrel": ["Plan B One-Step", "Mirena", "Kyleena", "Skyla", "Liletta"],
    "levosimendan": [],
    "levothyroxine": ["Synthroid", "Levoxyl", "Tirosint"],
    "lidocaine": ["Xylocaine"],
    "linaclotide": ["Linzess"],
    "linagliptin": ["Tradjenta"],
    "linezolid": ["Zyvox"],
    "liothyronine": ["Cytomel"],
    "liraglutide": ["Victoza", "Saxenda"],
    "lisdexamfetamine": ["Vyvanse"],
    "lisinopril": ["Prinivil", "Zestril"],
    "lisinopril-hydrochlorothiazide": ["Prinzide", "Zestoretic"],
    "lithium": ["Eskalith", "Lithobid"],
    "lixisenatide": ["Adlyxin"],
    "lomitapide": ["Juxtapid"],
    "loperamide": ["Imodium"],
    "lopinavir-ritonavir": ["Kaletra"],
    "loratadine": ["Claritin"],
    "lorazepam": ["Ativan"],
    "losartan": ["Cozaar"],
    "lubiprostone": ["Amitiza"],
    "lurasidone": ["Latuda"],
    "meclizine": ["Antivert", "Bonine"],
    "medroxyprogesterone": ["Depo-Provera"],
    "meloxicam": ["Mobic"],
    "mepolizumab": ["Nucala"],
    "meropenem": ["Merrem"],
    "meropenem-vaborbactam": ["Vabomere"],
    "mesalamine": ["Asacol", "Lialda", "Pentasa", "Rowasa", "Canasa"],
    "metformin": ["Glucophage"],
    "metformin-sitagliptin": ["Janumet"],
    "methadone": ["Dolophine"],
    "methimazole": ["Tapazole"],
    "methotrexate": ["Trexall", "Rasuvo", "Otrexup"],
    "methyldopa": ["Aldomet"],
    "methylphenidate": ["Ritalin", "Concerta", "Daytrana"],
    "metoclopramide": ["Reglan"],
    "metoprolol": ["Lopressor", "Toprol-XL"],
    "metronidazole": ["Flagyl"],
    "mexiletine": ["Mexitil"],
    "midazolam": ["Versed"],
    "midodrine": ["ProAmatine"],
    "mifepristone": ["Mifeprex", "Korlym"],
    "milrinone": ["Primacor"],
    "minocycline": ["Minocin"],
    "minoxidil": ["Rogaine"],
    "mirabegron": ["Myrbetriq"],
    "mirtazapine": ["Remeron"],
    "misoprostol": ["Cytotec"],
    "modafinil": ["Provigil"],
    "mometasone": ["Asmanex", "Nasonex"],
    "mometasone-formoterol": ["Dulera"],
    "montelukast": ["Singulair"],
    "morphine": ["MS Contin", "Kadian", "Duramorph"],
    "moxifloxacin": ["Avelox"],
    "moxifloxacin (ophthalmic)": ["Vigamox", "Moxeza"],
    "mycophenolate": ["CellCept", "Myfortic"],
    "nabumetone": ["Relafen"],
    "nadolol": ["Corgard"],
    "nafcillin": ["Nallpen"],
    "naloxegol": ["Movantik"],
    "naloxone": ["Narcan", "Kloxxado"],
    "naltrexone": ["ReVia", "Vivitrol"],
    "naltrexone-bupropion": ["Contrave"],
    "naproxen": ["Aleve", "Naprosyn"],
    "naratriptan": ["Amerge"],
    "nebivolol": ["Bystolic"],
    "neostigmine": ["Bloxiverz", "Prostigmin"],
    "netupitant-palonosetron": ["Akynzeo"],
    "niacin": ["Niaspan"],
    "nicardipine": ["Cardene"],
    "nifedipine": ["Procardia", "Adalat CC"],
    "nimodipine": ["Nymalize"],
    "nirmatrelvir-ritonavir": ["Paxlovid"],
    "nitrofurantoin": ["Macrobid", "Macrodantin"],
    "nitroglycerin": ["Nitrostat", "Nitro-Dur"],
    "nitroprusside": ["Nipride", "Nitropress"],
    "norepinephrine": ["Levophed"],
    "nortriptyline": ["Pamelor"],
    "nystatin": ["Mycostatin"],
    "octreotide": ["Sandostatin"],
    "ofloxacin": ["Floxin", "Ocuflox"],
    "olanzapine": ["Zyprexa"],
    "olanzapine-fluoxetine": ["Symbyax"],
    "olmesartan": ["Benicar"],
    "olmesartan-hydrochlorothiazide": ["Benicar HCT"],
    "olodaterol": ["Striverdi Respimat"],
    "olopatadine": ["Patanol", "Pataday"],
    "omadacycline": ["Nuzyra"],
    "omega-3-acid ethyl esters": ["Lovaza"],
    "omeprazole": ["Prilosec"],
    "ondansetron": ["Zofran"],
    "oritavancin": ["Orbactiv"],
    "orlistat": ["Xenical", "Alli"],
    "oseltamivir": ["Tamiflu"],
    "osimertinib": ["Tagrisso"],
    "oxaprozin": ["Daypro"],
    "oxazepam": ["Serax"],
    "oxcarbazepine": ["Trileptal"],
    "oxybutynin": ["Ditropan"],
    "oxycodone": ["Roxicodone", "OxyContin"],
    "oxycodone-acetaminophen": ["Percocet"],
    "ozanimod": ["Zeposia"],
    "paliperidone": ["Invega"],
    "palonosetron": ["Aloxi"],
    "pantoprazole": ["Protonix"],
    "paricalcitol": ["Zemplar"],
    "paroxetine": ["Paxil"],
    "patiromer": ["Veltassa"],
    "penicillin g benzathine": ["Bicillin L-A"],
    "penicillin v": ["Veetids"],
    "perampanel": ["Fycompa"],
    "phenazopyridine": ["Pyridium", "Azo"],
    "phenelzine": ["Nardil"],
    "phentermine-topiramate": ["Qsymia"],
    "phenylephrine": ["Neo-Synephrine"],
    "phenytoin": ["Dilantin"],
    "pimecrolimus": ["Elidel"],
    "pindolol": ["Visken"],
    "pioglitazone": ["Actos"],
    "piperacillin-tazobactam": ["Zosyn"],
    "pirfenidone": ["Esbriet"],
    "piroxicam": ["Feldene"],
    "pitavastatin": ["Livalo"],
    "plecanatide": ["Trulance"],
    "pramipexole": ["Mirapex"],
    "pramlintide": ["Symlin"],
    "prasugrel": ["Effient"],
    "pravastatin": ["Pravachol"],
    "prednisolone": ["Orapred", "Pred Forte"],
    "prednisone": ["Deltasone"],
    "pregabalin": ["Lyrica"],
    "procaine": ["Novocain"],
    "prochlorperazine": ["Compazine"],
    "promethazine": ["Phenergan"],
    "propafenone": ["Rythmol"],
    "propofol": ["Diprivan"],
    "propranolol": ["Inderal"],
    "propylthiouracil": ["PTU"],
    "pseudoephedrine": ["Sudafed"],
    "pyrazinamide": ["Tebrazid"],
    "quetiapine": ["Seroquel"],
    "quinupristin-dalfopristin": ["Synercid"],
    "raltegravir": ["Isentress"],
    "ramipril": ["Altace"],
    "ranolazine": ["Ranexa"],
    "rasagiline": ["Azilect"],
    "reteplase": ["Retavase"],
    "rifampin": ["Rifadin", "Rimactane"],
    "rifaximin": ["Xifaxan"],
    "riluzole": ["Rilutek"],
    "rimegepant": ["Nurtec ODT"],
    "risperidone": ["Risperdal"],
    "ritonavir": ["Norvir"],
    "rituximab": ["Rituxan"],
    "rivaroxaban": ["Xarelto"],
    "rizatriptan": ["Maxalt"],
    "rocuronium": ["Zemuron"],
    "roflumilast": ["Daliresp"],
    "romiplostim": ["Nplate"],
    "romosozumab": ["Evenity"],
    "rosiglitazone": ["Avandia"],
    "rosuvastatin": ["Crestor"],
    "rotigotine": ["Neupro"],
    "rufinamide": ["Banzel"],
    "sacubitril": [],
    "sacubitril-valsartan": ["Entresto"],
    "salbutamol": ["Ventolin"],
    "salmeterol": ["Serevent"],
    "salsalate": ["Disalcid"],
    "saxagliptin": ["Onglyza"],
    "scopolamine": ["Transderm Scop"],
    "selegiline": ["Eldepryl", "Zelapar"],
    "semaglutide": ["Ozempic", "Rybelsus", "Wegovy"],
    "sertraline": ["Zoloft"],
    "sevelamer": ["Renagel", "Renvela"],
    "sildenafil": ["Viagra"],
    "silodosin": ["Rapaflo"],
    "simvastatin": ["Zocor"],
    "sirolimus": ["Rapamune"],
    "sitagliptin": ["Januvia"],
    "sodium zirconium cyclosilicate": ["Lokelma"],
    "sofosbuvir-ledipasvir": ["Harvoni"],
    "sofosbuvir-velpatasvir": ["Epclusa"],
    "solifenacin": ["Vesicare"],
    "sotalol": ["Betapace", "Sorine"],
    "spironolactone": ["Aldactone"],
    "spironolactone-hydrochlorothiazide": ["Aldactazide"],
    "streptokinase": [],
    "succinylcholine": ["Anectine", "Quelicin"],
    "sucralfate": ["Carafate"],
    "sufentanil": ["Dsuvia", "Sufenta"],
    "sugammadex": ["Bridion"],
    "sulfasalazine": ["Azulfidine"],
    "sumatriptan": ["Imitrex"],
    "suvorexant": ["Belsomra"],
    "tacrolimus": ["Prograf", "Protopic"],
    "tadalafil": ["Cialis"],
    "tamoxifen": ["Nolvadex"],
    "tamsulosin": ["Flomax"],
    "tapentadol": ["Nucynta"],
    "tedizolid": ["Sivextro"],
    "telavancin": ["Vibativ"],
    "temazepam": ["Restoril"],
    "tenecteplase": ["TNKase"],
    "tenofovir alafenamide": ["Vemlidy"],
    "tenofovir disoproxil fumarate": ["Viread"],
    "terazosin": ["Hytrin"],
    "terbinafine": ["Lamisil"],
    "terbutaline": ["Brethine"],
    "teriparatide": ["Forteo"],
    "tesamorelin": ["Egrifta"],
    "theophylline": ["Theo-24", "Elixophyllin"],
    "ticagrelor": ["Brilinta"],
    "ticlopidine": ["Ticlid"],
    "timolol": ["Timoptic"],
    "tiotropium": ["Spiriva"],
    "tiotropium-olodaterol": ["Stiolto Respimat"],
    "tirofiban": ["Aggrastat"],
    "tirzepatide": ["Mounjaro", "Zepbound"],
    "tizanidine": ["Zanaflex"],
    "tobramycin": ["Nebcin", "Tobrex"],
    "tocilizumab": ["Actemra"],
    "tofacitinib": ["Xeljanz"],
    "tolcapone": ["Tasmar"],
    "tolterodine": ["Detrol"],
    "topiramate": ["Topamax"],
    "toremifene": ["Fareston"],
    "torsemide": ["Demadex"],
    "tramadol": ["Ultram"],
    "tranexamic acid": ["Cyklokapron", "Lysteda"],
    "tranylcypromine": ["Parnate"],
    "travoprost": ["Travatan Z"],
    "trazodone": ["Desyrel", "Oleptro"],
    "triamcinolone": ["Kenalog"],
    "triamterene": ["Dyrenium"],
    "triamterene-hydrochlorothiazide": ["Dyazide", "Maxzide"],
    "trihexyphenidyl": ["Artane"],
    "trimethoprim-sulfamethoxazole": ["Bactrim", "Septra"],
    "trimipramine": ["Surmontil"],
    "trospium": ["Sanctura"],
    "ubrogepant": ["Ubrelvy"],
    "ulipristal": ["Ella"],
    "umeclidinium": ["Incruse Ellipta"],
    "umeclidinium-vilanterol": ["Anoro Ellipta"],
    "uricosuric": [],
    "ustekinumab": ["Stelara"],
    "valacyclovir": ["Valtrex"],
    "valproate sodium": ["Depacon"],
    "valproic acid": ["Depakene", "Depakote"],
    "valsartan": ["Diovan"],
    "vancomycin": ["Vancocin"],
    "vardenafil": ["Levitra", "Staxyn"],
    "varenicline": ["Chantix"],
    "vecuronium": ["Norcuron"],
    "vedolizumab": ["Entyvio"],
    "venlafaxine": ["Effexor"],
    "verapamil": ["Calan", "Verelan"],
    "vernakalant": [],
    "vibegron": ["Gemtesa"],
    "vilazodone": ["Viibryd"],
    "voriconazole": ["Vfend"],
    "vorinostat": ["Zolinza"],
    "vortioxetine": ["Trintellix"],
    "warfarin": ["Coumadin", "Jantoven"],
    "zafirlukast": ["Accolate"],
    "zaleplon": ["Sonata"],
    "zavegepant": ["Zavzpret"],
    "zidovudine": ["Retrovir"],
    "ziprasidone": ["Geodon"],
    "zoledronic acid": ["Reclast", "Zometa"],
    "zolmitriptan": ["Zomig"],
    "zolpidem": ["Ambien"]
}

def _build_regex(cfg, lib):
    CS = bool(cfg.get("case_sensitive"))
    def _norm(s): return s if CS else s.lower()
    norm_map = {_norm(k): list(dict.fromkeys(v)) for k, v in lib.items()}
    keys = sorted(norm_map.keys(), key=len, reverse=True)
    flags = 0 if CS else re.IGNORECASE
    rx = re.compile(r"\b(" + "|".join(map(re.escape, keys)) + r")\b", flags) if keys else None
    return norm_map, rx

def _already_has_brand(text: str, end_idx: int, brands):
    look = text[end_idx:end_idx+80]
    i = 0
    while i < len(look) and look[i].isspace():
        i += 1
    if i < len(look) and look[i] == "(":
        close = look.find(")", i+1)
        if close != -1:
            inside = look[i+1:close].lower()
            for b in brands:
                if b.lower() in inside:
                    return True
    return False

def _augment(text: str) -> str:
    cfg = _get_cfg()
    lib = dict(LIBRARY_MAP)
    em = cfg.get("extra_map") or {}
    if isinstance(em, dict):
        for k, v in em.items():
            lib[k] = v if isinstance(v, list) else [str(v)]
    norm_map, RX = _build_regex(cfg, lib)
    if not RX:
        return text
    delim = cfg.get("delimiter", "; ")
    fmt = cfg.get("insert_format", " {brandparen}")
    flag = cfg.get("debug_flag", "")
    def repl(m):
        g = m.group(0)
        brands = norm_map.get(g if cfg.get("case_sensitive") else g.lower(), [])
        if not brands or _already_has_brand(text, m.end(), brands):
            return g
        return g + fmt.format(brandparen="(" + delim.join(brands) + ")") + flag
    try:
        return RX.sub(repl, text)
    except Exception:
        return text

def _on_card_will_show(text, card, kind):
    try:
        cfg = _get_cfg()
        deck_ok, tag_ok = True, True
        if cfg.get("exclude_decks"):
            nm = (mw.col.decks.name_or_none(card.did) or "").lower()
            deck_ok = all(not nm.startswith(p.lower()) for p in cfg["exclude_decks"])
        if cfg.get("exclude_tags"):
            tags = set(card.note().tags or [])
            tag_ok = not any(t in tags for t in cfg["exclude_tags"])
        
        if not (deck_ok and tag_ok):
            return text
        return _augment(text)
    except Exception:
        return text

card_will_show.append(_on_card_will_show)

# ----------------- UI -----------------

class AdvancedDialog(QDialog):
    def __init__(self, cfg, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Advanced Options")
        self.cfg = cfg
        lay = QVBoxLayout(self)
        form = QFormLayout()
        self.case_cb = QCheckBox("Match case (case-sensitive)")
        self.case_cb.setChecked(bool(cfg.get("case_sensitive")))
        self.delim = QLineEdit(cfg.get("delimiter", "; "))
        self.insfmt = QLineEdit(cfg.get("insert_format", " {brandparen}"))
        self.debug = QLineEdit(cfg.get("debug_flag", ""))
        form.addRow(self.case_cb)
        form.addRow("Delimiter:", self.delim)
        form.addRow("Insert format:", self.insfmt)
        form.addRow("Debug flag:", self.debug)
        lay.addLayout(form)
        box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        qconnect(box.accepted, self.accept)
        qconnect(box.rejected, self.reject)
        lay.addWidget(box)
    def apply(self):
        self.cfg["case_sensitive"] = bool(self.case_cb.isChecked())
        self.cfg["delimiter"] = self.delim.text()
        self.cfg["insert_format"] = self.insfmt.text()
        self.cfg["debug_flag"] = self.debug.text()

class StreamlinedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(ADDON_NAME)
        self.resize(700, 750)
        self.cfg = _get_cfg()
        root = QVBoxLayout(self)

        root.addWidget(QLabel("<b>Add New Drugs:</b>"))
        drug_row = QHBoxLayout()
        self.generic_le = QLineEdit(); self.generic_le.setPlaceholderText("Generic")
        self.brand_le = QLineEdit(); self.brand_le.setPlaceholderText("Brand(s); separate with ';'")
        add_drug_btn = QPushButton("Add Drug"); qconnect(add_drug_btn.clicked, self._on_add_drug)
        drug_row.addWidget(self.generic_le); drug_row.addWidget(self.brand_le); drug_row.addWidget(add_drug_btn)
        root.addLayout(drug_row)

        self.drug_list = QListWidget(); root.addWidget(self.drug_list)
        drug_ctrl = QHBoxLayout()
        edit_btn = QPushButton("Edit Selected"); del_drug_btn = QPushButton("Delete Selected")
        qconnect(edit_btn.clicked, self._on_edit_drug); qconnect(del_drug_btn.clicked, self._on_delete_drug)
        drug_ctrl.addWidget(edit_btn); drug_ctrl.addWidget(del_drug_btn); drug_ctrl.addStretch()
        root.addLayout(drug_ctrl)

        excl_layout = QHBoxLayout()
        tag_col = QVBoxLayout()
        tag_col.addWidget(QLabel("<b>Exclude Tags:</b>"))
        tag_in = QHBoxLayout()
        self.tag_le = QLineEdit(); self.tag_le.setPlaceholderText("tag_name")
        add_tag_btn = QPushButton("+"); qconnect(add_tag_btn.clicked, self._on_add_tag)
        tag_in.addWidget(self.tag_le); tag_in.addWidget(add_tag_btn)
        tag_col.addLayout(tag_in)
        self.tag_list = QListWidget(); tag_col.addWidget(self.tag_list)
        del_tag_btn = QPushButton("Remove Tag"); qconnect(del_tag_btn.clicked, self._on_del_tag)
        tag_col.addWidget(del_tag_btn)
        
        deck_col = QVBoxLayout()
        deck_col.addWidget(QLabel("<b>Exclude Decks (Prefix):</b>"))
        deck_in = QHBoxLayout()
        self.deck_le = QLineEdit(); self.deck_le.setPlaceholderText("Deck::Subdeck")
        add_deck_btn = QPushButton("+"); qconnect(add_deck_btn.clicked, self._on_add_deck)
        deck_in.addWidget(self.deck_le); deck_in.addWidget(add_deck_btn)
        deck_col.addLayout(deck_in)
        self.deck_list = QListWidget(); deck_col.addWidget(self.deck_list)
        del_deck_btn = QPushButton("Remove Deck"); qconnect(del_deck_btn.clicked, self._on_del_deck)
        deck_col.addWidget(del_deck_btn)

        excl_layout.addLayout(tag_col); excl_layout.addLayout(deck_col)
        root.addLayout(excl_layout)

        bottom = QHBoxLayout()
        adv_btn = QPushButton("Advanced Options…"); qconnect(adv_btn.clicked, self._on_advanced)
        box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        qconnect(box.accepted, self._on_save); qconnect(box.rejected, self.reject)
        bottom.addWidget(adv_btn); bottom.addStretch(); bottom.addWidget(box)
        root.addLayout(bottom)

        self._refresh_all()

    def _refresh_all(self):
        self.drug_list.clear()
        emap = self.cfg.get("extra_map", {})
        for g, b in sorted(emap.items()):
            it = QListWidgetItem(f"{g} → {'; '.join(b)}"); it.setData(32, g)
            self.drug_list.addItem(it)
        
        self.tag_list.clear()
        for t in self.cfg.get("exclude_tags", []):
            self.tag_list.addItem(t)
            
        self.deck_list.clear()
        for d in self.cfg.get("exclude_decks", []):
            self.deck_list.addItem(d)

    def _on_add_drug(self):
        g, b = self.generic_le.text().strip(), self.brand_le.text().strip()
        if g and b:
            self.cfg.setdefault("extra_map", {})[g] = [s.strip() for s in b.split(";") if s.strip()]
            self.generic_le.clear(); self.brand_le.clear(); self._refresh_all()

    def _on_edit_drug(self):
        it = self.drug_list.currentItem()
        if not it: return
        gen = it.data(32)
        cur = "; ".join(self.cfg["extra_map"].get(gen, []))
        text, ok = QInputDialog.getText(self, "Edit Brands", f"Brands for {gen}:", text=cur)
        if ok:
            self.cfg["extra_map"][gen] = [s.strip() for s in text.split(";") if s.strip()]
            self._refresh_all()

    def _on_delete_drug(self):
        it = self.drug_list.currentItem()
        if it:
            del self.cfg["extra_map"][it.data(32)]; self._refresh_all()

    def _on_add_tag(self):
        t = self.tag_le.text().strip()
        if t and t not in self.cfg["exclude_tags"]:
            self.cfg["exclude_tags"].append(t)
            self.tag_le.clear(); self._refresh_all()

    def _on_del_tag(self):
        it = self.tag_list.currentItem()
        if it:
            self.cfg["exclude_tags"].remove(it.text()); self._refresh_all()

    def _on_add_deck(self):
        d = self.deck_le.text().strip()
        if d and d not in self.cfg["exclude_decks"]:
            self.cfg["exclude_decks"].append(d)
            self.deck_le.clear(); self._refresh_all()

    def _on_del_deck(self):
        it = self.deck_list.currentItem()
        if it:
            self.cfg["exclude_decks"].remove(it.text()); self._refresh_all()

    def _on_advanced(self):
        dlg = AdvancedDialog(self.cfg, self)
        if dlg.exec():
            dlg.apply()

    def _on_save(self):
        _save_cfg(self.cfg); self.accept()

def on_config_action():
    dlg = StreamlinedDialog(mw)
    dlg.exec()

action = mw.form.menuTools.addAction(ADDON_NAME)
qconnect(action.triggered, on_config_action)

mw.addonManager.setConfigAction(__name__, on_config_action)