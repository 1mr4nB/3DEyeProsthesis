#import
import os
import subprocess
import sys
#import 3maticCode

#Try
try:
    import trimatic
except:
    in_3matic = False
else:
    in_3matic = True
    
if not in_3matic:
    
    ############################# Our mimics code    
    
    source = r"E:\studenten\2021eyeprosthesis\3Deyeprosthesis\DICOM\21101811\28110001"    # Check scan 03, 
    dicoms = mimics.file.import_dicom_images(source_folder=source)


    mask = mimics.segment.create_mask()
    mask.name = "Oogleegte"

    HU_min = -1024
    HU_max = -250

    GV_min = mimics.segment.HU2GV(HU_min)
    GV_max = mimics.segment.HU2GV(HU_max)

    #Thresholding
    mimics.segment.threshold(mask=mask, threshold_min=GV_min, threshold_max=GV_max)


    #originvect = [-47.5,-31.5,-3]
    
    #xvect = [30,0,0]
    #yvect = [0,20,0]
    #zvect = [0,0,25]


    #boundingbox = mimics.BoundingBox3d(origin=originvect,first_vector=xvect,second_vector=yvect,third_vector=zvect)
    #mimics.segment.crop_mask(mask,bounding_box=boundingbox)
    
    msg = "Snijd de mask bij via SEGMENT > Crop Mask > Draw"
    mimics.dialogs.message_box(msg,ui_blocking=False)


    #Calculate part

    part = mimics.segment.calculate_part(mask=mask, quality='High')
    part.name = 'oogholte'
    
    ################################ Our mimics code    
        
    #mimics.file.export_part(object_to_convert=part, file_name=r"E:\studenten\oogholte_part.stl")


    #Export in 3matic
    root_path_of_script = os.path.split(os.path.abspath(__file__))[0]
    path_of_stl = os.path.join(root_path_of_script,part.name + ".stl")
    mimics.file.export_part(part,path_of_stl)
    with open(os.path.join(os.path.split(__file__)[0],"my_temp.txt"),"w") as f:
        f.write(path_of_stl)
        f.write("File is created!\n")
        
    #Prepare to run 3-matic    
    trimatic = mimics.file.get_path_to_3matic()
    command = trimatic
    args = ("-run_script", __file__, path_of_stl,f.name)
    process = subprocess.Popen((command,) + args, shell=False, stdout=subprocess.PIPE)
    #process.wait()
    with open(f.name, "r")as f:
        lines = f.readlines()
        os.remove(f.name)
        for i in range(2):
            mimics.file.import_stl(lines[i + 1].strip())

else:
    path_of_stl = sys.argv[1]
    f = sys.argv[2]
    trimatic.import_part_stl(path_of_stl)
    
    #part = trimatic.find_parts(part.name)
    #if part:
    #    plane = trimatic.create_plane_fit(part[0])
    #    cut_parts = trimatic.cut(part[0], plane)
    #    exp = trimatic.export_stl_ascii(cut_parts, os.path.split(os.path.abspath(__file__))[0])
    #    with open(f, "a") as f:
    #        f.write(exp[0] + "\n")
    #        f.write(exp[1])
    #
    #        print("To continue please close 3-matic!")
    
    ###################### Here comes our 3-matic code (see other file)
    
    Oogleegte_object = trimatic.find_object("oogholte")
    Oogleegte_object = trimatic.filter_small_shells(Oogleegte_object)
    
    ObjectTuple = trimatic.split_surface(Oogleegte_object)

    for m in range(0,len(ObjectTuple)):
        surface = ObjectTuple[m]
        if (surface != ObjectTuple[0]):
            index = ObjectTuple.index(surface)
            trimatic.delete(Oogleegte_object.find_surface("Surface-" + str(index)))
    
    trimatic.smooth(Oogleegte_object)

    trimatic.message_box(message="Vul alle gaten op (via methode in document) en klik op OK",title="Gaten checken", with_cancel=True)

    msg = "Markeer het vooroppervlak van het oog via: Mark (Wave Brush Mark) + Smooth Marking Border (klik op OK eerst)"
    trimatic.message_box(message=msg,title="Mark", with_cancel=True)

    marked_triangles = trimatic.activate_mark_wave_brush()

    if len(Oogleegte_object.get_curves()) > 1:
        trimatic.message_box(message="Zoek de juiste curve en verwijder de rest", title="Curve", with_cancel=True)
        curves = Oogleegte_object.find_curve("Curve")
        surface = trimatic.split_surfaces_by_curves(curves=curves)
    
    trimatic.message_box(message="Het object is gesplitst, HIDE alle onnodige surfaces en SHOW de juiste surface", title="Achterzijde surface", with_cancel=True)
    
    ObjectTuple = trimatic.split_surface(Oogleegte_object)

    for i in range(0, len(ObjectTuple)):
        if ObjectTuple[i].visible == False:
            pass
        elif ObjectTuple[i].visible == True:
            oogholte = trimatic.copy_to_part(ObjectTuple[i], None)
        

    #oogholte = trimatic.copy_to_part(surface[0], None)  # CHECKEN: Is surface[0] altijd het geval?
    oogholte.name = "anophthalmic"

    trimatic.message_box(message="Bridgen via FIX>CREATE BRIDGE + FILL HOLE FREEFORM", title= "Bridging technique", with_cancel=True)

    oogholte.merge_all_surfaces()

    trimatic.smooth(oogholte)
    trimatic.smooth(oogholte)

    

    #surface[0].name = "achterzijde"
    
    #trimatic.smooth(Oogleegte_object)
    #trimatic.smooth(Oogleegte_object)


    Oogleegte_object.visible = False
    
    
    #Sla het project op (als 3-matic project) om samen te voegen met Intact Oogbol
    filename = r"E:\studenten\P&O BMT\Intact oog Mimics File\Oogholte.mxp"

    trimatic.save_project(filename)
    
    
    ######################s


