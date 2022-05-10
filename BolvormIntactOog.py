source = r"E:\studenten\2021eyeprosthesis\3Deyeprosthesis\DICOM\21101811\28110000"
dicoms = mimics.file.import_dicom_images(source_folder=source)

#Mask creëeren                                                                            ###################### Huidmask
maskHuid = mimics.segment.create_mask()
maskHuid.name = "Huid"

HU_min = -718
HU_max = -177

GV_min = mimics.segment.HU2GV(HU_min)
GV_max = mimics.segment.HU2GV(HU_max)

#Thresholding
mimics.segment.threshold(mask=maskHuid, threshold_min=GV_min, threshold_max=GV_max)


#Crop
#originvect = [13.122604, -8.982759, 25.658207]
originvect = [14,-38.5, -8.84]

xvect = [31.16,0,0]
yvect = [0,29.52,0]
zvect = [0,0,31]

boundingbox = mimics.BoundingBox3d(origin=originvect,first_vector=xvect,second_vector=yvect,third_vector=zvect)
mimics.segment.crop_mask(maskHuid,bounding_box=boundingbox)

partHuid = mimics.segment.calculate_part(maskHuid)
partHuid.name = "Huidweefsel"



#Spier                                                                                    ###################### Spiermask

maskSpier = mimics.segment.create_mask()
maskSpier.name = "Spierweefsel"

HU_min_spier = -5
HU_max_spier =  135

GV_min = mimics.segment.HU2GV(HU_min_spier)
GV_max = mimics.segment.HU2GV(HU_max_spier)

#Thresholding
mimics.segment.threshold(mask=maskSpier, threshold_min=GV_min, threshold_max=GV_max)


#Crop

originvect = [14,-38.5, -8.84]

xvect = [30,0,0]
yvect = [0,40,0]
zvect = [0,0,31]


boundingbox = mimics.BoundingBox3d(origin=originvect,first_vector=xvect,second_vector=yvect,third_vector=zvect)
mimics.segment.crop_mask(maskSpier,bounding_box=boundingbox)

#part maken

partSpier = mimics.segment.calculate_part(maskSpier)
partSpier.name = "Spierweefsel"


#2 masks uniten
m1 = maskHuid
m2 = maskSpier
m = mimics.segment.boolean_operations(mask_a=m1, mask_b=m2, operation="Unite")

#Van de gigamask een part maken
partHuidSpier = mimics.segment.calculate_part(m)
partHuidSpier.name = "HuidSpier"


#mimics.analyze.create_sphere_fit_to_surface(part = part)
#mimics.analyze.create_sphere_fit_to_surface(part = partHuid)
#mimics.analyze.create_sphere_fit_to_surface(part = partSpier)

t = "Indicate sphere"
sph = mimics.analyze.indicate_sphere(title=t, message='Please indicate four points that will define sphere.', show_message_box=True,confirm=True)
sph.name = "Oogbol"

#center: [28.813646, -23.185680, 10.416167]
#radius: 12.7359
#sphere -> mask ->part


### Schedel                                                                            ######################### Schedelmask

maskSchedel = mimics.segment.create_mask()
maskSchedel.name = "Schedel"

HU_min_schedel = 649
HU_max_schedel = 3413

GV_min_schedel = mimics.segment.HU2GV(HU_min_schedel)
GV_max_schedel = mimics.segment.HU2GV(HU_max_schedel)

#Thresholding
mimics.segment.threshold(mask=maskSchedel, threshold_min=GV_min_schedel, threshold_max=GV_max_schedel)


#Part maken

partSchedel = mimics.segment.calculate_part(maskSchedel)
partSchedel.name = "Schedel"


partHuid.visible = False                # De 3D-parts onzichtbaar maken
partSpier.visible = False
partHuidSpier.visible = False


f = r"E:\studenten\P&O BMT\Intact oog Mimics File\IntactOogBol.mcs"
t = "Mimics Project Files"
mimics.file.save_project(filename=f,save_as_type=t)


