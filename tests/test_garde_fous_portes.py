"""Témoins conformes et dégradés pour les contrôles portés de Containers."""

import base64
import binascii
import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def charger(nom):
    return runpy.run_path(str(ROOT / "tests" / nom))


def test_indices_valides_puis_langue_absente_et_encodage_invalide(tmp_path, monkeypatch):
    module = charger("test_hints_ecrits.py")
    fonction = module["test_les_deux_langues_sont_renseignees"]
    monkeypatch.setitem(fonction.__globals__, "LABS", tmp_path)
    dossier = tmp_path / "temoin/challenge"
    dossier.mkdir(parents=True)
    def encode(texte):
        return base64.b64encode(texte.encode()).decode()
    indices = [{"cost": c, "text_en": encode("Inspect the state"), "text_fr": encode("Examinez l'état")} for c in module["COUTS_ATTENDUS"]]

    def ecrire():
        (dossier / "hints.yaml").write_text(yaml.safe_dump({"hints": indices}), encoding="utf-8")

    ecrire()
    fonction("temoin")
    module["test_quatre_indices_de_cout_croissant"]("temoin")
    indices[0]["text_fr"] = ""
    ecrire()
    assert module["indices_en_clair"]("temoin")[0]["fr"] == "", "La dégradation doit être présente."
    with pytest.raises(AssertionError, match="sans texte français"):
        fonction("temoin")
    indices[0]["text_fr"] = "%%%"
    ecrire()
    with pytest.raises(binascii.Error):
        module["indices_en_clair"]("temoin")
    assert module["porte_le_gabarit"]([{"en": "Nudge to write", "fr": "Indice"}]), "Le gabarit doit être vu."
    assert not module["porte_le_gabarit"]([{"en": "Inspect the state", "fr": "Examinez l'état"}]), "Un indice rédigé doit passer."


def test_solution_chiffree_puis_solution_lisible(tmp_path):
    fonction = charger("test_solutions_chiffrees.py")["test_la_solution_est_chiffree"]
    fonction.__globals__["RACINE"] = tmp_path
    fonction.__globals__["SOLUTIONS"] = tmp_path
    fichier = tmp_path / "solution.yaml"
    fichier.write_bytes(b"$ANSIBLE_VAULT;1.1;AES256\n00\n")
    fonction(fichier)
    fichier.write_text("tasks: []\n", encoding="utf-8")
    assert not fichier.read_bytes().startswith(b"$ANSIBLE_VAULT"), "Le clair doit être constaté avant le verdict."
    with pytest.raises(AssertionError, match="n'est pas chiffré"):
        fonction(fichier)


def test_style_texte_valide_puis_cadratin(tmp_path, monkeypatch):
    module = charger("test_style_apprenant.py")
    fonction = module["test_pas_de_tiret_cadratin"]
    monkeypatch.setitem(fonction.__globals__, "LABS", tmp_path)
    fichier = tmp_path / "scenario.fr.md"
    fichier.write_text("Examinez l'état : corrigez la ressource.", encoding="utf-8")
    fonction(fichier)
    fichier.write_text("Examinez " + chr(0x2014) + " corrigez.", encoding="utf-8")
    assert chr(0x2014) in fichier.read_text(encoding="utf-8"), "Le cadratin doit être présent."
    with pytest.raises(AssertionError, match="tiret"):
        fonction(fichier)


def test_maturite_solution_et_squelette(tmp_path, monkeypatch):
    module = charger("test_maturite_des_labs.py")
    fonction = module["test_un_lab_ecrit_porte_une_solution_de_reference"]
    monkeypatch.setitem(fonction.__globals__, "SOLUTIONS", tmp_path)
    with pytest.raises(AssertionError, match="AUCUNE solution"):
        fonction("temoin")
    (tmp_path / "temoin").mkdir()
    (tmp_path / "temoin/solution.yaml").write_text("encrypted witness", encoding="utf-8")
    fonction("temoin")
    with pytest.raises(AssertionError, match="encore le squelette"):
        module["test_un_squelette_ne_porte_pas_de_solution"]("temoin")


def test_parcours_oublie_fantome_doublon_et_lab_ampute(tmp_path, monkeypatch):
    module = charger("test_meta_declare_les_labs.py")
    fonction = module["test_chaque_lab_livre_est_declare_dans_le_parcours"]
    monkeypatch.setitem(fonction.__globals__, "LABS", tmp_path / "labs")
    monkeypatch.setitem(fonction.__globals__, "META", tmp_path / "meta.yml")
    lab = tmp_path / "labs/temoin"
    lab.mkdir(parents=True)
    for nom in module["ATTENDUS"]:
        fichier = lab / nom
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text("id: temoin\n", encoding="utf-8")

    def parcours(labs):
        (tmp_path / "meta.yml").write_text(yaml.safe_dump({"sections": [{"labs": labs}]}), encoding="utf-8")

    parcours(["temoin"])
    fonction()
    module["test_aucun_repertoire_de_lab_n_est_ampute"]()
    parcours([])
    assert not module["_declares"](), "L'omission doit être constatée avant le verdict."
    with pytest.raises(AssertionError, match=r"absent.*parcours"):
        fonction()
    parcours(["temoin", "fantome"])
    with pytest.raises(AssertionError, match=r"absent.*labs/"):
        module["test_chaque_lab_declare_existe_vraiment"]()
    parcours(["temoin", "temoin"])
    with pytest.raises(AssertionError, match="plusieurs fois"):
        module["test_aucun_lab_n_est_declare_deux_fois"]()
    parcours(["temoin"])
    (lab / "lab.yaml").unlink()
    with pytest.raises(AssertionError, match="incomplet"):
        module["test_aucun_repertoire_de_lab_n_est_ampute"]()


def test_chemin_du_controleur_est_lu_dans_le_code(tmp_path, monkeypatch):
    module = charger("test_briefs_pointent_juste.py")
    fonction = module["workdir_declare"]
    monkeypatch.setitem(fonction.__globals__, "LABS", tmp_path)
    lab = tmp_path / "temoin"
    (lab / "tools").mkdir(parents=True)
    (lab / "lab.yaml").write_text("runtime: {type: vm}\n", encoding="utf-8")
    controller = lab / "tools/controller.py"
    controller.write_text('class Controller:\n def __init__(self):\n  self.work = self.lab / "challenge/work"\n', encoding="utf-8")
    assert fonction("temoin") == "challenge/work", "Le chemin réellement consommé doit être reconnu."
    controller.write_text('# challenge/work est seulement un commentaire\n', encoding="utf-8")
    assert fonction("temoin") == "", "Un commentaire ne doit pas déclarer un répertoire de travail."


def test_promesse_critique_sans_declaration(tmp_path, monkeypatch):
    module = charger("test_exigence_critique_declaree.py")
    lab = tmp_path / "temoin"
    lab.mkdir()
    (lab / "lab.yaml").write_text("lab_type: capstone\n", encoding="utf-8")
    (lab / "scenario.fr.md").write_text("Aucun total ne compense ce défaut.", encoding="utf-8")
    assert module["_promesses"](lab), "La promesse dégradée doit être découverte."
    with pytest.raises(AssertionError, match="ne la déclare"):
        module["test_une_promesse_ecrite_a_sa_declaration"](lab)
    (lab / "lab.yaml").write_text("exam_blocking_checks: [test_critique]\n", encoding="utf-8")
    module["test_une_promesse_ecrite_a_sa_declaration"](lab)


def test_hadolint_cible_le_catalogue_et_refuse_une_erreur(tmp_path, monkeypatch, capsys):
    module = runpy.run_path(str(ROOT / "scripts/hooks/hadolint_cible.py"))
    appels = []
    resultat = SimpleNamespace(returncode=0)
    monkeypatch.setattr(module["subprocess"], "run", lambda args, **kw: appels.append(args) or resultat)
    assert module["controler"](tmp_path) == 0, "Sans Dockerfile le contrôle est sans objet."
    assert "N/A" in capsys.readouterr().out, "L'absence de mesure doit être explicite."
    (tmp_path / "fixtures").mkdir()
    (tmp_path / "fixtures/Dockerfile").write_text("FROM intentionally:broken", encoding="utf-8")
    assert not module["dockerfiles"](tmp_path), "Une fixture ne doit pas être corrigée par le hook."
    fichier = tmp_path / "Dockerfile"
    fichier.write_text("FROM invalid:base", encoding="utf-8")
    assert module["dockerfiles"](tmp_path) == [fichier], "Le Dockerfile fautif doit être ciblé."
    assert module["controler"](tmp_path) == 0, "Un verdict hadolint conforme doit être accepté."
    resultat.returncode = 1
    assert resultat.returncode == 1, "Le refus doit être constaté avant la mesure."
    assert module["controler"](tmp_path) == 1, "Le refus de hadolint doit être propagé."
    assert appels == [["hadolint", str(fichier)]] * 2, "Le hook doit analyser le fichier réel."
