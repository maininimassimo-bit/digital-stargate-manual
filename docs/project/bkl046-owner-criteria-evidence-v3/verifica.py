"""Rebuild Owner criteria v3 without promoting any criterion."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path

REGISTRATION="6dd023aab7485e2314bae19c68b2d6c40e78a67a7661dc992909012ea562157b"
ACTIONS=json.loads("[[[\"ledgerV88\",\"indexV88\"],\"coperturaSemantica\",\"Verificare la copertura del dominio riaperto sui requisiti autorevoli, includendo i casi privi di risultati.\",\"studio\"],[[\"ledgerV88\"],\"coperturaSemantica\",\"Collegare prerequisiti, parametri, maschere e decisioni dei workflow alle prove comportamentali per processo.\",\"studio\"],[[\"ledgerV88\",\"romanRange\"],\"validazioneScientifica\",\"Verificare evidenze e limiti a livello di criterio, senza trasferire le misure Roman ad altri domini.\",\"studio\"],[[\"ledgerV88\",\"nativeOffline\",\"romanRange\"],\"validazioneScientifica\",\"Completare verifiche di versione, equivalenza dei domini e prove native con ricevute ammesse.\",\"studio e revisori indipendenti\"],[[\"ledgerV88\",\"romanRange\",\"nativeOffline\"],\"validazioneScientifica\",\"Riconciliare successi, rifiuti e correzioni per criterio. Conservare anche i 1.920 confronti fuori gamma.\",\"studio\"],[[\"indexV88\",\"joinedReplay\"],\"riletturaGitHub\",\"Verificare dipendenze e impronte a partire dalla destinazione effettiva approvata.\",\"verifica VM dopo decisione di distribuzione\"],[[\"indexV88\"],\"baselineFinale\",\"Accettare il file finale dopo il riscontro integrale dei criteri applicabili.\",\"studio e Owner\"],[[\"ledgerV88\"],\"coperturaSemantica\",\"Rileggere la logica utilizzabile nella conoscenza consolidata e valutarla sull’intero dominio.\",\"studio\"],[[\"ledgerV88\",\"indexV88\"],\"baselineFinale\",\"Conservare le decisioni aperte fino alle rispettive evidenze di accettazione.\",\"studio e Owner\"],[[\"indexV88\"],\"riletturaGitHub\",\"Verificare storico e vincoli operativi nel file finale e nella copia di destinazione.\",\"verifica VM dopo decisione di distribuzione\"],[[\"joinedReplay\",\"indexV88\"],\"riletturaGitHub\",\"Ricostruire il file finale e tutte le versioni storiche a partire dagli asset effettivi.\",\"verifica VM dopo decisione di distribuzione\"],[[\"ledgerV88\",\"indexV88\"],\"riletturaGitHub\",\"Verificare copertura di documenti, protocolli, script e logica per byte e dipendenze sulla destinazione.\",\"verifica VM dopo decisione di distribuzione\"],[[\"ledgerV88\",\"nativeOffline\",\"romanRange\"],\"riletturaGitHub\",\"Verificare disponibilità remota di tutti gli esiti originali, inclusi rifiuti e correzioni.\",\"verifica VM dopo decisione di distribuzione\"],[[\"indexV88\",\"joinedReplay\"],\"riletturaGitHub\",\"Riconciliare l’insieme effettivo degli artefatti consegnati e le dipendenze.\",\"verifica VM dopo decisione di distribuzione\"],[[\"indexV88\",\"joinedReplay\"],\"riletturaGitHub\",\"Verificare ID, dimensione, impronta e legami di ruolo, versione e dipendenze degli oggetti consegnati.\",\"verifica VM dopo decisione di distribuzione\"],[[\"indexV88\",\"joinedReplay\"],\"decisioneDistribuzione\",\"Identificare destinazione privata e perimetro approvato per il corpus, poi verificare la presenza dei byte remoti.\",\"Owner per decisione, VM per verifica\"],[[\"joinedReplay\"],\"riletturaGitHub\",\"Riscaricare gli 81 asset dell’inventario intermedio autorizzato e ricostruire le parti usando gli stessi byte.\",\"verifica VM dopo decisione di distribuzione\"],[[\"joinedReplay\",\"ledgerV88\"],\"riletturaGitHub\",\"Riprodurre dalla destinazione effettiva i percorsi richiesti dai protocolli e recuperare lo storico.\",\"verifica VM dopo decisione di distribuzione\"],[[\"ledgerV88\",\"indexV88\"],\"coperturaSemantica\",\"Verificare la catena requisito, protocollo, prova, esito e decisione nell’intera baseline consegnata.\",\"studio e verifica VM\"]]")


def need(ok, why):
    if not ok:
        raise ValueError(why)


def read(path, pin):
    raw=path.read_bytes()
    need(sha256(raw).hexdigest()==pin, "Changed bytes: "+path.name)
    return raw


def build(root):
    sources=root/"fonti"
    manifest=json.loads(read(sources/"registrazione.json",REGISTRATION))
    docs={}
    for key,ref in manifest.items():
        raw=read(sources/(key+".json"),ref["sha256"])
        need(len(raw)==ref["bytes"],"Changed byte count: "+key)
        docs[key]=json.loads(raw)
    old=docs["parentMatrix"]
    ids=[row["id"] for row in old["criteria"]]
    ledger=docs["ledgerV88"]
    need(ids==[row["id"] for row in ledger["ownerCriteria"]]
         and len(ids)==len(set(ids))==len(ACTIONS)==old["openCriteria"]==19,"Owner criterion universe")
    need(all(r["status"]=="NOT_YET_SATISFIED" for r in old["criteria"]+ledger["ownerCriteria"]),
         "Unexpected disposition")
    coverage=ledger["coverage"]
    need((coverage["requirements"],coverage["criteria"],coverage["scientificFamiliesOpen"],
          coverage["scientificAxesOpen"],coverage["scientificClosures"])==(4920,14521,7,25,0),"Ledger scope")
    index=docs["indexV88"]
    need(index["version"]=="1.171" and index["releaseState"]=="INTERIM_REGISTERED_BASELINE"
         and not index["delivery"]["integralTransferVerified"]
         and not index["delivery"]["finalKnowledgeAccepted"],"Index disposition")
    replay=docs["joinedReplay"]
    need(replay["scope"]=="offline" and (replay["verifiedAssetCount"],replay["verifiedObjects"],
         replay["verifiedLogicalAliases"])==(81,10180,11839) and not replay["githubReadbackAndReplayVerified"],
         "Delivery proof scope")
    native=docs["nativeOffline"]
    need(native["nativeExecutions"]==0 and not native["independentApprovalsReceived"]
         and not native["nativeAdmissionRequested"],"Native proof scope")
    roman=docs["romanRange"]
    need(sum(r["signalMatched"] for r in roman["summary"])==960
         and sum(r["outsideGainRange"] for r in roman["summary"])==1920
         and not roman["calibratedDoseMatched"],"Roman transfer proof scope")
    criteria=[]
    updated={k:v for k,v in manifest.items() if k!="parentMatrix"}
    for row,(links,stage,next_action,owner) in zip(old["criteria"],ACTIONS,strict=True):
        need(set(links)<=updated.keys(),"Dangling evidence")
        criteria.append(dict(row,partialEvidence=row["partialEvidence"]+links,
                             nextVerification=dict(stage=stage,responsibility=owner,evidenceNeeded=next_action)))
    result=dict(old,schema="BKL046_OWNER_CRITERIA_EVIDENCE_MATRIX_V3",
                precedingMatrixSha256=manifest["parentMatrix"]["sha256"],
                evidence=dict(old["evidence"],**updated),criteria=criteria,
                sourceLedgerV88Sha256=manifest["ledgerV88"]["sha256"])
    need(result["openCriteria"]==19 and result["criteriaPromoted"]==result["scientificClosures"]==0,
         "Unexpected closure")
    return (json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()


def main():
    cli=ArgumentParser(description=__doc__)
    cli.add_argument("root",type=Path)
    cli.add_argument("--build",action="store_true")
    a=cli.parse_args()
    data=build(a.root)
    target=a.root/"BKL-046-MATRICE-CRITERI-v3.json"
    if a.build:
        with target.open("xb") as f:
            f.write(data)
    need(target.read_bytes()==data,"Owner matrix replay differs")
    print(json.dumps(dict(ownerCriteriaVerified=19,promoted=0,newEvidenceSources=5)))


if __name__=="__main__":
    main()