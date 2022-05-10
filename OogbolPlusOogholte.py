import trimatic
OogBolFile = r"E:\studenten\P&O BMT\Intact oog Mimics File\IntactOogBol.mcs"
OogholteFile = r"E:\studenten\P&O BMT\Intact oog Mimics File\Oogholte.mxp"
LensOG = r"E:\studenten\P&O BMT\Intact oog Mimics File\LensOrigineel.mxp"
LensGroot = r"E:\studenten\P&O BMT\Intact oog Mimics File\LensGroot.mxp"
LensKlein = r"E:\studenten\P&O BMT\Intact oog Mimics File\LensKlein.mxp"
OogLens = r"E:\studenten\P&O BMT\Intact oog Mimics File\LensFinaal.mxp"

trimatic.import_project(OogBolFile)
trimatic.import_project(OogholteFile)
trimatic.import_project(LensOG)
trimatic.import_project(LensGroot)
trimatic.import_project(LensKlein)
trimatic.import_project(OogLens)

bol = trimatic.find_object("Oogbol")
#oogholte = trimatic.find_object("oogholte")
anophthalmic = trimatic.find_object("anophthalmic")
schedel = trimatic.find_object("Schedel")
lens1 = trimatic.find_object("SCLERAL LENS")
lens2 = trimatic.find_object("LensGroot")
lens3 = trimatic.find_object("LensKlein")
lens = trimatic.find_object("LensFinaal")
bol_copy = trimatic.duplicate(bol)
mirrored_sphere = trimatic.mirror(bol_copy, origin=(0,0,0), normal=(3,0,0))




bolPart = trimatic.create_sphere_part(bol_copy.center, bol_copy.radius)
bolPart.name = "OogBolPart"
bolPart.transparency = 0.5

trimatic.delete(bol)
#trimatic.delete(bol_copy) # Nog nodig later
bol_copy.visible = False
schedel.visible = False
lens1.visible = False
lens2.visible = False
lens3.visible = False
lens.visible = False

trimatic.activate_translate_rotate(bolPart) # OK: Druk op ESC om te exiten


anoph_surface = anophthalmic.get_surfaces()[0]
print(anoph_surface)
uitgerokken_anoph = trimatic.move_surface(anoph_surface, direction=None, distance=-8.0, solid=True)

trimatic.activate_translate_rotate(bolPart) # OK: Druk op ESC om te exiten

anophthalmic.color = (255/255,255/255,0)
bolPart.color = (51/255,153/255,255/255)

#bolPart_copy = trimatic.duplicate(bolPart)
#bolPart_copy.name = "oogbolkopie"
#bolPart_copy.visible = False

oogprothese = trimatic.boolean_intersection([anophthalmic, bolPart])
oogprothese.name = "oogprothese"


print(oogprothese.get_surfaces())

for surface in oogprothese.get_surfaces():
    if surface.get_parent().name == "OogBolPart":
        c = surface.get_border().get_contours()
print(c)
c = list(c)
print(c)
#c = oogprothese.find_surface("OogBolPart").get_border().get_contours()
trimatic.finish.smooth_edge(entities = c[0], distance=0.5, smooth_detail=trimatic.SmoothDetail.Coarse)  # Enkel ÃƒÂ©ÃƒÂ©n keer smooth_edge werkt?
#trimatic.finish.smooth_edge(entities = c[1], distance=0.5, smooth_detail=trimatic.SmoothDetail.Coarse)


lens.visible = True
trimatic.message_box(message="Plaats de (kleinste) lens op de juiste positie > Klikken (druk op OK eerst)", title="Lenscheck", with_cancel=True)

coords = ()
while len(coords) == 0:
    try:
        coords = trimatic.indicate_coordinate()
    except:
        break
print(coords)
print(lens.object_coordinate_system)

vector1 = lens.dimension_min
vector2 = coords
translation_vector = (-(vector1[0]-vector2[0]), -(vector1[1]-vector2[1]), -(vector1[2]-vector2[2]))

trimatic.translate(lens, translation_vector)


#trimatic.message_box(message="Als de gewilde lens op Show staat, klik op OK", title="Interactive", with_cancel=True)


#trimatic.split_surfaces_by_curves(entities=oogholte)





#plane = trimatic.create_plane_fit(oogholte)
#plane.delta_x = 20
#plane.delta_y = 20

#curve = trimatic.create_intersection_curve(bolPart,plane)
#part1, part2 = trimatic.cut(bolPart, plane)
#part1.name = "Juiste halfbol"
#part2.name = "Foute halfbol"
#part2.visible = False
#plane.visible = False
#trimatic.delete(plane)
#opp = trimatic.find_surface("OogBolPart")
#trimatic.delete(opp)
#part3,part4 = trimatic.surfaces_to_parts(part1)
#trimatic.delete(part4)
#part3.name = "Halfbol"
#trimatic.delete(part1)

#halfbol = part1
#c = trimatic.create_point(bol_copy.center)
#c.name = "Volle bol Center"
#[normal, closest] = trimatic.compute_normal_and_closest_point(parts=part1, point=c)
#point1 = trimatic.create_point(closest)
#point1.name = "Halfbol Center"
#point2 = trimatic.create_point((closest[0] + normal[0], closest[1] + normal[1], closest[2] + normal[2]))
#point2.name = "Normaalvector"

#path = trimatic.create_curve([point1,point2])
#path.name = "Normal path"
#sweep_loft_part = trimatic.sweep_loft(start_profile=part1,end_profile=oogholte,path=path)




#oogholtesurf = oogholte.find_surface("Surface-0")
#print(oogholtesurf)
#halfbolsurf = halfbol.find_surface("Surface")
#print(halfbolsurf)

#print(halfbolsurf.get_border())
#print(halfbolsurf.get_border().get_contours())
#halfbolsurfcontour = halfbolsurf.get_border().get_contours()[0]
#print(oogholtesurf.get_border())
#print(oogholtesurf.get_border().get_contours())
#oogholtesurfcontour = oogholtesurf.get_border().get_contours()[0]

#curve = trimatic.create_curve(points=[(0,0,0),plane.normal])

#sweep_loft_part = trimatic.sweep_loft(start_profile=halfbolsurfcontour,end_profile=oogholtesurfcontour,path=curve)

#analmax = trimatic.compute_extrema_analysis_points(entities=oogholte, direction=plane.normal, minima=False, global_extrema_only = False)
#print(analmax)
#analmax = list(analmax)
#print(analmax)
#print(plane.normal)
#analcurve = trimatic.create_curve(analmax)




