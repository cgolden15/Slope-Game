import UnityPy as unitypy, sys

bundle_path = sys.argv[1] if len(sys.argv) > 1 else "extracted/data/data.unity3d"
env = unitypy.load(bundle_path)
for obj in env.objects:
    if obj.type.name == "Font":
        data = obj.read()
        name = getattr(data, "name", None) or getattr(data, "m_Name", "?")
        fd = getattr(data, "m_FontData", None)
        size = len(fd) if fd else 0
        print("Font:", repr(name), "path_id=%d" % obj.path_id, "font_data=%d bytes" % size)
