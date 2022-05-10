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

# Vanaf hier: UV Map (handmatig) op oogprothese object
trimatic.message_box(message="Handmatig nu: UV Map op oogprothese object", title="UV Map Texturing", with_cancel=True)
