extends Control

onready var PersonnalisaitonSauvKiPiou = $PersonnalisaitonSauvKiPiou
onready var PersonnalisationEntrainement = $PersonnalisaitonEntrainement

var calibration_thread : Thread
var modeJeuSelected

onready var gauche = $PersonnalisaitonSauvKiPiou/Lieu_apparition/Label_Gauche/Gauche
onready var droite = $PersonnalisaitonSauvKiPiou/Lieu_apparition/Label_Droite/Droite
onready var bas = $PersonnalisaitonSauvKiPiou/Lieu_apparition/Label_Bas/Bas
onready var haut = $PersonnalisaitonSauvKiPiou/Lieu_apparition/Label_Haut/Haut
onready var cam = $MarginContainer/VBoxContainer/HBoxContainer2/Affichage_cam/HBoxContainer/affichage_cam
onready var couleur_jeu = $MarginContainer/VBoxContainer/HBoxContainer/Couleur_Jeu_Node

onready var couleur_selected = $Couleur_Select
onready var couleur_selected_1 = $IndicateurEquipe/Couleur_Equipe_1
onready var couleur_selected_2 = $IndicateurEquipe/Couleur_Equipe_2

onready var fond = $TextureRect

func _ready():
	
	fond.texture = load(Autoloader.bg_path)
	
	couleur_selected_1.visible = false
	couleur_selected_2.visible = false
	
	PersonnalisaitonSauvKiPiou.visible = false
	PersonnalisationEntrainement.visible = false
	
	var lower = Vector3(170, 100, 100)  
	var upper = Vector3(179, 255, 255)  
	
	Autoloader.upperColor_1 = Vector3(179, 255, 255) 
	Autoloader.lowerColor_1 = Vector3(170, 100, 100)  

	Autoloader.upperColor_2 = Vector3(140, 255, 255)  
	Autoloader.lowerColor_2 = Vector3(100, 100, 100) 
	
	var autoloader = get_node("/root/Autoloader")
	autoloader.set_color_range(lower, upper)
	pass

func _on_Button_Calibrer_pressed():
	if !Autoloader.is_calibrated:
		Autoloader.start_calibration()

func _on_Button_Retour_pressed():
	Autoloader.stop_calibration()
	get_tree().change_scene("res://Scenes/Main_Menu.tscn")
	pass

func _on_Button_Jouer_pressed():
	var autoloader = get_node("/root/Autoloader")
	
	# Mettre à jour les directions basées sur les cases à cocher
	autoloader.gauche = gauche.pressed
	autoloader.droite = droite.pressed
	autoloader.haut = haut.pressed
	autoloader.bas = bas.pressed
	autoloader.cam = cam.pressed

	# Vérifier si la partie doit commencer avec un temps
	if autoloader.avec_temps and autoloader.temps <= 0:
		return  # Ne pas commencer la partie si le temps est 0 et qu'on joue avec le temps
	
	# Vérifier si la calibration est faite et les probabilités sont correctes
	if autoloader.is_calibrated:
		if autoloader.piou_proba + autoloader.moskigros_proba + autoloader.moskito_proba == 100:
			if modeJeuSelected == "SauvKi_Piou":
				get_tree().change_scene("res://Scenes/Mode_Jeu/Jeu_Mode_SauvKiPiou.tscn")
			elif modeJeuSelected == "Entrainement":
				get_tree().change_scene("res://Scenes/Mode_Jeu/mode_Jeu_Entrainement.tscn")
	
func _on_Button_Red_pressed():
	Autoloader.is_red = true
	Autoloader.couleur_selected = "Rouge"
	var lower = Vector3(170, 100, 100)  
	var upper = Vector3(179, 255, 255)  
	var autoloader = get_node("/root/Autoloader")
	autoloader.set_color_range(lower, upper)

func _on_Button_Jaune_pressed():
	Autoloader.couleur_selected = "Jaune"
	Autoloader.is_red = false
	var lower = Vector3(20, 100, 100)  
	var upper = Vector3(30, 255, 255)  
	var autoloader = get_node("/root/Autoloader")
	autoloader.set_color_range(lower, upper)

func _on_Button_Vert_pressed():
	Autoloader.couleur_selected = "Vert"
	Autoloader.is_red = false
	var lower = Vector3(35, 100, 100)  
	var upper = Vector3(85, 255, 255)  
	var autoloader = get_node("/root/Autoloader")
	autoloader.set_color_range(lower, upper)

func _on_Button_Bleu_pressed():
	Autoloader.couleur_selected = "Bleu"
	Autoloader.is_red = false
	var lower = Vector3(100, 100, 100) 
	var upper = Vector3(140, 255, 255)  
	var autoloader = get_node("/root/Autoloader")
	autoloader.set_color_range(lower, upper)

func _on_SauvKi_Piou_pressed():
	modeJeuSelected = "SauvKi_Piou"
	PersonnalisaitonSauvKiPiou.visible = true
	PersonnalisationEntrainement.visible = false
	print("Mode de jeu sélectionné : " + modeJeuSelected)

func _on_Entrainement_pressed():
	
	Autoloader.avec_equipe = false
	couleur_jeu.visible = true
	couleur_selected_1.visible = false
	couleur_selected_2.visible = false
	couleur_selected.visible = true
	
	modeJeuSelected = "Entrainement"
	PersonnalisaitonSauvKiPiou.visible = false
	PersonnalisationEntrainement.visible = true
	print("Mode de jeu sélectionné : " + modeJeuSelected)


func _on_Remove_Temps30_pressed():
	if (Autoloader.temps - 30) >= 0 and Autoloader.avec_temps == true:
		Autoloader.temps -= 30 

func _on_Remove_Temps15_pressed():
	if (Autoloader.temps - 15) >= 0 and Autoloader.avec_temps == true:
		Autoloader.temps -= 15 

func _on_Add_Temps15_pressed():
	if Autoloader.avec_temps == true:
		Autoloader.temps += 15 

func _on_Add_Temps30_pressed():
	if Autoloader.avec_temps == true:
		Autoloader.temps += 30 

func _on_Sans_Temps_pressed():
	Autoloader.avec_temps = false
	Autoloader.temps = 0

func _on_Avec_Temps_pressed():
	Autoloader.avec_temps = true

func _on_Add_Freq_SauvKiPiou_pressed():
	Autoloader.freq_apparition_sauvkipiou +=0.5

func _on_Rm_Freq_SauvKiPiou_pressed():
	if Autoloader.freq_apparition_sauvkipiou - 0.5 > 0:
		Autoloader.freq_apparition_sauvkipiou -=0.5

#=== MOSKITO ===#

func _on_Add_speed_Min_Moskito_pressed():
	if Autoloader.moskito_speed_min +10 <= Autoloader.moskito_speed_max:
		Autoloader.moskito_speed_min += 10

func _on_Add_speed_Max_Moskito_pressed():
	Autoloader.moskito_speed_max += 10 
	
func _on_Rm_speed_Min_Moskito_pressed():
	Autoloader.moskito_speed_min -= 10 
	
func _on_Rm_speed_Max_Moskito_pressed():
	if Autoloader.moskito_speed_max -10 >= Autoloader.moskito_speed_min:
		Autoloader.moskito_speed_max -= 10 

func _on_Add_Taille_Moskito_pressed():
	Autoloader.moskito_scale_percent += 0.1

func _on_Rm_Taille_Moskito_pressed():
	if Autoloader.moskito_scale_percent - 0.1 >= 0.5:
		Autoloader.moskito_scale_percent -= 0.1

func _on_Add_Pts_Moskito_pressed():
	Autoloader.moskito_pts_value += 1

func _on_Rm_Pts_Moskito_pressed():
	Autoloader.moskito_pts_value -= 1

func _on_Add_Proba_Moskito_pressed():
	if Autoloader.moskito_proba + 5 <= 100:
		Autoloader.moskito_proba += 5

func _on_RmProba_Moskito_pressed():
	if Autoloader.moskito_proba - 5 >= 0:
		Autoloader.moskito_proba -= 5

#=== MOSKIGROS ===#

func _on_Add_speed_Min_Moskigros_pressed():
	if Autoloader.moskigros_speed_min +10 <= Autoloader.moskigros_speed_max:
		Autoloader.moskigros_speed_min += 10

func _on_Add_speed_Max_Moskigros_pressed():
	Autoloader.moskigros_speed_max += 10 

func _on_Rm_speed_Min_Moskigros_pressed():
	Autoloader.moskigros_speed_min -= 10 


func _on_Rm_speed_Max_Moskigros_pressed():
	if Autoloader.moskigros_speed_max -10 >= Autoloader.moskigros_speed_min:
		Autoloader.moskigros_speed_max -= 10 

func _on_Add_Taille_Moskigros_pressed():
	Autoloader.moskigros_scale_percent += 0.1

func _on_Rm_Taille_Moskigros_pressed():
	if Autoloader.moskigros_scale_percent - 0.1 >= 0.5:
		Autoloader.moskigros_scale_percent -= 0.1

func _on_Add_Pts_Moskigros_pressed():
	Autoloader.moskigros_pts_value += 1

func _on_Rm_Pts_Moskigros_pressed():
	Autoloader.moskigros_pts_value -= 1

func _on_Add_Proba_Moskigros_pressed():
	if Autoloader.moskigros_proba + 5 <= 100:
		Autoloader.moskigros_proba += 5

func _on_RmProba_Moskigros_pressed():
	if Autoloader.moskigros_proba - 5 >= 0:
		Autoloader.moskigros_proba -= 5


#=== PIOU ===#

func _on_Add_speed_Min_Piou_pressed():
	if Autoloader.piou_speed_min +10 <= Autoloader.piou_speed_max:
		Autoloader.piou_speed_min += 10

func _on_Add_speed_Max_Piou_pressed():
	Autoloader.piou_speed_max += 10 

func _on_Rm_speed_Min_Piou_pressed():
	Autoloader.piou_speed_min -= 10 

func _on_Rm_speed_Max_Piou_pressed():
	if Autoloader.piou_speed_max -10 >= Autoloader.piou_speed_min:
		Autoloader.piou_speed_max -= 10 

func _on_Add_Taille_Piou_pressed():
	Autoloader.piou_scale_percent += 0.1

func _on_Rm_Taille_Piou_pressed():
	if Autoloader.piou_scale_percent - 0.1 >= 0.5:
		Autoloader.piou_scale_percent -= 0.1
		
func _on_Add_Pts_Piou_pressed():
	Autoloader.piou_pts_value += 1

func _on_Rm_Pts_Piou_pressed():
	Autoloader.piou_pts_value -= 1

func _on_Add_Proba_Piou_pressed():
	if Autoloader.piou_proba + 5 <= 100:
		Autoloader.piou_proba += 5

func _on_RmProba_Piou_pressed():
	if Autoloader.piou_proba - 5 >= 0:
		Autoloader.piou_proba -= 5


#=== CIBLE  ===#

func _on_Add_Taille_Cible_pressed():
	Autoloader.cible_scale_percent += 0.1

func _on_Rm_Taille_Cible_pressed():
	if Autoloader.cible_scale_percent - 0.1 >= 0.5:
		Autoloader.cible_scale_percent -= 0.1

func _on_Add_Freq_pressed():
	Autoloader.freq_apparition += 0.5

func _on_Rm_Freq_pressed():
	if Autoloader.freq_apparition - 0.5 > 0:
		Autoloader.freq_apparition -= 0.5

func _on_Rm_Cible_pressed():
	if Autoloader.max_target - 1 > 0:
		Autoloader.max_target -= 1

func _on_Add_Cible_pressed():
	Autoloader.max_target += 1

#=== EQUIPE ===#

func _on_Sans_Equipe_pressed():
	Autoloader.avec_equipe = false
	couleur_jeu.visible = true
	couleur_selected_1.visible = false
	couleur_selected_2.visible = false
	couleur_selected.visible = true

func _on_Avec_Equipe_pressed():
	Autoloader.avec_equipe = true
	couleur_jeu.visible = false
	couleur_selected_1.visible = true
	couleur_selected_2.visible = true
	couleur_selected.visible = false
	
	modeJeuSelected = "SauvKi_Piou"
	PersonnalisaitonSauvKiPiou.visible = true
	PersonnalisationEntrainement.visible = false
	print("Mode de jeu sélectionné : " + modeJeuSelected)

func _on_Button_Jaune_1_pressed():
	if Autoloader.couleur_selected_2 != "Jaune":
		Autoloader.couleur_selected_1 = "Jaune"
		
		Autoloader.upperColor_1 = Vector3(30, 255, 255) 
		Autoloader.lowerColor_1 = Vector3(20, 100, 100)


func _on_Button_Bleu_1_pressed():
	if Autoloader.couleur_selected_2 != "Bleu":
		Autoloader.couleur_selected_1 = "Bleu"

		Autoloader.upperColor_1 = Vector3(140, 255, 255)
		Autoloader.lowerColor_1 = Vector3(100, 100, 100)


func _on_Button_Vert_1_pressed():
	if Autoloader.couleur_selected_2 != "Vert":
		Autoloader.couleur_selected_1 = "Vert"

		Autoloader.upperColor_1 = Vector3(35, 100, 100)
		Autoloader.lowerColor_1 = Vector3(85, 255, 255)


func _on_Button_Red_1_pressed():
	if Autoloader.couleur_selected_2 != "Rouge":
		Autoloader.couleur_selected_1 = "Rouge"

		Autoloader.upperColor_1 = Vector3(179, 255, 255)  
		Autoloader.lowerColor_1 = Vector3(170, 100, 100)


func _on_Button_Jaune_2_pressed():
	if Autoloader.couleur_selected_1 != "Jaune":
		Autoloader.couleur_selected_2 = "Jaune"

		Autoloader.upperColor_2 = Vector3(30, 255, 255) 
		Autoloader.lowerColor_2 = Vector3(20, 100, 100)

func _on_Button_Bleu_2_pressed():
	if Autoloader.couleur_selected_1 != "Bleu":
		Autoloader.couleur_selected_2 = "Bleu"

		Autoloader.upperColor_2 = Vector3(140, 255, 255)
		Autoloader.lowerColor_2 = Vector3(100, 100, 100)


func _on_Button_Vert_2_pressed():
	if Autoloader.couleur_selected_1 != "Vert":
		Autoloader.couleur_selected_2 = "Vert"

		Autoloader.upperColor_2 = Vector3(35, 100, 100)
		Autoloader.lowerColor_2 = Vector3(85, 255, 255)

func _on_Button_Red_2_pressed():
	if Autoloader.couleur_selected_1 != "Rouge":
		Autoloader.couleur_selected_2 = "Rouge"
		
		Autoloader.upperColor_2 = Vector3(179, 255, 255)  
		Autoloader.lowerColor_2 = Vector3(170, 100, 100)
