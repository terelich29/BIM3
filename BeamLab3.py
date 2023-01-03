import NemAll_Python_Geometry as g
import NemAll_Python_BaseElements as be
import NemAll_Python_BasisElements as bes


def check_allplan_version(build_ele, version):
    del build_ele
    del version
    return True


def create_element(build_ele, doc):
    element = Beam(doc)
    return element.create(build_ele)


class Beam:
    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, build_ele):
        self.union(build_ele)
        self.l_p(build_ele)
        return (self.model_ele_list, self.handle_list)

    def get_all_data(self, build_ele):
        mew = build_ele.mew.value
        lws = build_ele.lws.value
        lwsc = build_ele.lwsc.value
        mw = build_ele.mw.value
        lhs = build_ele.lhs.value
        mh = build_ele.mh.value
        tws = build_ele.tws.value
        ths = build_ele.ths.value
        bl = build_ele.bl.value
        lt = build_ele.lt.value
        i = build_ele.i.value
        return [mew, lws, lwsc, mw, lhs, mh, tws, ths, bl, lt, i]

    def union(self, build_ele):
        style = be.CommonProperties()
        style.GetGlobalProperties()
        style.Pen = 1
        style.Color = 3
        style.Stroke = 1
        d = self.l_p(build_ele)
        m = self.m_p(build_ele)
        u = self.t_p(build_ele)
        e, f = g.MakeUnion(d, m)
        e, f = g.MakeUnion(f, u)
        self.model_ele_list.append(bes.ModelElement3D(style, f))

    def l_p(self, build_ele):
        f = self.l_1(build_ele)
        e, f = g.MakeUnion(f, self.l_2(build_ele))
        e, f = g.MakeUnion(f, self.l_3(build_ele))
        e, f = g.MakeUnion(f, self.l_4(build_ele))
        e, f = g.MakeUnion(f, self.l_2_2(build_ele))
        e, f = g.MakeUnion(f, self.l_3_2(build_ele))
        e, f = g.MakeUnion(f, self.l_4_2(build_ele))
        e, f = g.MakeUnion(f, self.l_2_3(build_ele))
        e, f = g.MakeUnion(f, self.l_3_3(build_ele))
        e, f = g.MakeUnion(f, self.l_2_4(build_ele))
        e, f = g.MakeUnion(f, self.l_3_4(build_ele))
        e, f = g.MakeUnion(f, self.l__l(build_ele))
        return f

    def t_p(self, build_ele):
        p = (build_ele.bl.value - build_ele.mew.value)
        f = self.t_1(build_ele)
        e, f = g.MakeUnion(f, self.t_3(build_ele))
        e, f = g.MakeUnion(f, self.t_2(build_ele))
        e, f = g.MakeUnion(f, self.t_3(build_ele, p=p))
        e, f = g.MakeUnion(f, self.t_4(build_ele))
        e, f = g.MakeUnion(f, self.t_2_2(build_ele))
        e, f = g.MakeUnion(f, self.t_4(build_ele, build_ele.lws.value - build_ele.lwsc.value * 2, build_ele.tws.value, 10))
        e, f = g.MakeUnion(f, self.t_2_3(build_ele))
        e, f = g.MakeUnion(f, self.t_4_2(build_ele))
        e, f = g.MakeUnion(f, self.t_4_2(build_ele, build_ele.lws.value - build_ele.lwsc.value * 2, build_ele.tws.value, 10))
        e, f = g.MakeUnion(f, self.t_3_3(build_ele))
        e, f = g.MakeUnion(f, self.t__l(build_ele))
        return f

    def m_p(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(0, all_data[0], all_data[1])
        pl += g.Point3D(0, all_data[2] - all_data[0], all_data[1])
        pl += g.Point3D(all_data[3], all_data[2] - all_data[0], all_data[1])
        pl += g.Point3D(all_data[3] + all_data[4], all_data[2] - all_data[0] - (all_data[2] - all_data[0] * 2 - all_data[5]) / 2, all_data[1])
        pl += g.Point3D(all_data[6] - (all_data[3] + all_data[4]), all_data[2] - all_data[0] - (all_data[2] - all_data[0] * 2 - all_data[5]) / 2, all_data[1])
        pl += g.Point3D(all_data[6] - all_data[3], all_data[2] - all_data[0], all_data[1])
        pl += g.Point3D(all_data[6], all_data[2] - all_data[0], all_data[1])
        pl += g.Point3D(all_data[6], all_data[0], all_data[1])
        pl += g.Point3D(all_data[6] - all_data[3], all_data[0], all_data[1])
        pl += g.Point3D(all_data[6] - all_data[3] - all_data[4], all_data[0] + (all_data[2] - all_data[0] * 2 - all_data[5]) / 2, all_data[1])
        pl += g.Point3D(all_data[3] + all_data[4], all_data[0] + (all_data[2] - all_data[0] * 2 - all_data[5]) / 2, all_data[1])
        pl += g.Point3D(all_data[3], all_data[0], all_data[1])
        pl += g.Point3D(0, all_data[0], all_data[1])

        dir = g.Polyline3D()
        dir += g.Point3D(0, all_data[0], all_data[1])
        dir += g.Point3D(0, all_data[0], all_data[1] + build_ele.mh.value)

        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def t_1(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[0], all_data[6] - (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0], -(all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0], all_data[2] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])

        e, f = g.CreatePolyhedron(pl, dir)

        return f

    def t_2(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4] + all_data[5])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2 + (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[8] - all_data[0] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] + (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4] + all_data[5])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1] -  all_data[2], all_data[4] + all_data[5])
        dir += g.Point3D(all_data[8] - all_data[0] + 10, all_data[1] - all_data[2] - 10, all_data[4] + all_data[5] + 10)

        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def t_3(self, build_ele, p=0):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(p, all_data[2], all_data[4] + all_data[5])
        pl += g.Point3D(p, all_data[1] - all_data[2], all_data[4] + all_data[5])
        pl += g.Point3D(p, all_data[1] + (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(p, -(all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(p, all_data[2], all_data[4] + all_data[5])

        dir = g.Polyline3D()
        dir += g.Point3D(p, all_data[2], all_data[4] + all_data[5])
        dir += g.Point3D(p + all_data[0], all_data[2], all_data[4] + all_data[5])

        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def t_4(self, build_ele, minus_1=0, minus_2=0, digit=-10):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2] - minus_1, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[6] - (all_data[6] - all_data[1]) / 2 - minus_2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[8] - all_data[0] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] + (all_data[6] - all_data[1]) / 2 - minus_2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2] - minus_1, all_data[4] + all_data[5])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2] - minus_1, all_data[4] + all_data[5])
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2] + digit - minus_1, all_data[4] + all_data[5])
        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def t_2_2(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4] + all_data[5])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9], all_data[2] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, (all_data[1] - all_data[2] * 2 - all_data[3]) / 2 - (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[8] - all_data[0] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, -(all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[8] - all_data[0],  all_data[2], all_data[4] + all_data[5])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4] + all_data[5])
        dir += g.Point3D(all_data[8] - all_data[0] + 10, all_data[2] + 10, all_data[4] + all_data[5] + 10)

        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def t_2_3(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4] + all_data[5])
        pl += g.Point3D(all_data[0] + all_data[9], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[0] + all_data[9] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2 + (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] + (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4] + all_data[5])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4] + all_data[5])
        dir += g.Point3D(all_data[0] - 10, all_data[1] - all_data[2] - 10, all_data[4] + all_data[5] - 10)
        e, f = g.CreatePolyhedron(pl, dir)
        
        return f

    def t_4_2(self, build_ele, minus_1=0, minus_2=0, digit=-10):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2] - minus_1, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[0], all_data[1] + (all_data[6] - all_data[1]) / 2 - minus_2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] + (all_data[6] - all_data[1]) / 2 - minus_2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2] - minus_1, all_data[4] + all_data[5])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[1] - all_data[2] - minus_1, all_data[4] + all_data[5])
        dir += g.Point3D(all_data[0], all_data[1] - all_data[2] - minus_1 + digit, all_data[4] + all_data[5])

        e, f = g.CreatePolyhedron(pl, dir)

        return f

    def t_3_3(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[2], all_data[4] + all_data[5])
        pl += g.Point3D(all_data[0] + all_data[9], all_data[2] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] + all_data[5])
        pl += g.Point3D(all_data[0] + all_data[9] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, (all_data[1] - all_data[2] * 2 - all_data[3]) / 2 - (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, -(all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(all_data[0], all_data[2], all_data[4] + all_data[5])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[2], all_data[4] + all_data[5])
        dir += g.Point3D(all_data[0] - 10, all_data[2] + 10, all_data[4] + all_data[5] - 10)

        e, f = g.CreatePolyhedron(pl, dir)

        return f

    def t__l(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(0, -(all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(0, all_data[6] - (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(0, all_data[6] - (all_data[6] - all_data[1]) /2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(0, all_data[6] - (all_data[6] - all_data[1]) / 2 - all_data[10], all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(0, all_data[6] - (all_data[6] - all_data[1]) / 2 - all_data[10], all_data[4] + all_data[5] + all_data[7] + build_ele.hp.value)
        pl += g.Point3D(0, - (all_data[6] - all_data[1]) / 2 + all_data[10], all_data[4] + all_data[5] + all_data[7] + build_ele.hp.value)
        pl += g.Point3D(0, - (all_data[6] - all_data[1]) / 2 + all_data[10], [4] + all_data[5] + all_data[7])
        pl += g.Point3D(0, - (all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        pl += g.Point3D(0, -(all_data[6] - all_data[1]) / 2,  all_data[4] + all_data[5] + all_data[7])

        dir = g.Polyline3D()
        dir += g.Point3D(0, -(all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        dir += g.Point3D(all_data[8], -(all_data[6] - all_data[1]) / 2, all_data[4] + all_data[5] + all_data[7])
        e, f = g.CreatePolyhedron(pl, dir)

        return f

    def l_1(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4])
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2 - all_data[3], all_data[4])
        pl += g.Point3D(all_data[0], 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0], all_data[1], all_data[4] - all_data[10])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[1], all_data[4] - all_data[10])
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1], all_data[4] - all_data[10])
        e, f = g.CreatePolyhedron(pl, dir)

        return f

    def l_2(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4])
        pl += g.Point3D(all_data[0] + all_data[9], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4])
        pl += g.Point3D(all_data[0] + all_data[9] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4])
        dir += g.Point3D(all_data[0] - 10, all_data[1] - all_data[2] - 10, all_data[4] - 10)

        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def l_3(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(0, all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(0, all_data[1] - all_data[2], all_data[4])
        pl += g.Point3D(0, all_data[2], all_data[4])
        pl += g.Point3D(0, 0, all_data[4] - all_data[10])
        pl += g.Point3D(0, all_data[1], all_data[4] - all_data[10])

        dir = g.Polyline3D()
        dir += g.Point3D(0, all_data[1], all_data[4] - all_data[10])
        dir += g.Point3D(all_data[0], all_data[1], all_data[4] - all_data[10])

        e, f = g.CreatePolyhedron(pl, dir)
 
        return f

    def l_4(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4])
        pl += g.Point3D(all_data[0], all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[1] - all_data[2], all_data[4])
        dir += g.Point3D(all_data[0], all_data[1] - all_data[2] - 10, all_data[4])

        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def l_2_2(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[2], all_data[4])
        pl += g.Point3D(all_data[0] + all_data[9], all_data[2] + ( all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4])
        pl += g.Point3D(all_data[0] + all_data[9] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0], all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[2], all_data[4])
        dir += g.Point3D(all_data[0] - 10, all_data[2] + 10, all_data[4] - 10)

        e, f = g.CreatePolyhedron(pl, dir)
 
        return f

    def l_3_2(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0], 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1], all_data[4] - all_data[10])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1], all_data[4] - all_data[10])
        dir += g.Point3D(all_data[8], all_data[1], all_data[4] - all_data[10])

        e, f = g.CreatePolyhedron(pl, dir) 
        return f

    def l_4_2(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[0], all_data[2], all_data[4])
        pl += g.Point3D(all_data[0], 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[0], all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[0], all_data[2], all_data[4])
        dir += g.Point3D(all_data[0], all_data[2] + 10, all_data[4])

        e, f = g.CreatePolyhedron(pl, dir) 
        return f

    def l_2_3(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9], all_data[1] - all_data[2] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4])
        dir += g.Point3D(all_data[8] - all_data[0] + 10, all_data[1] - all_data[2] - 10, all_data[4] + 10)

        e, f = g.CreatePolyhedron(pl, dir)
 
        return f

    def l_3_3(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0] - (all_data[1] - all_data[2] *  2 - all_data[3]) / 2, all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2], all_data[4])
        dir += g.Point3D(all_data[8] - all_data[0], all_data[1] - all_data[2] - 10, all_data[4])

        e, f = g.CreatePolyhedron(pl, dir)
        return f

    def l_2_4(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9], all_data[2] + (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0] - all_data[9] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4])
        dir += g.Point3D(all_data[8] - all_data[0] - 10, all_data[2] + 10, all_data[4] - 10)

        e, f = g.CreatePolyhedron(pl, dir)
 
        return f

    def l_3_4(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4])
        pl += g.Point3D(all_data[8] - all_data[0], 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0] - (all_data[1] - all_data[2] * 2 - all_data[3]) / 2, 0, all_data[4] - all_data[10])
        pl += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4])

        dir = g.Polyline3D()
        dir += g.Point3D(all_data[8] - all_data[0], all_data[2], all_data[4])
        dir += g.Point3D(all_data[8] - build_ele.mew.value, all_data[2] + 10, all_data[4])

        e, f = g.CreatePolyhedron(pl, dir)
 
        return f

    def l__l(self, build_ele):
        all_data = self.get_all_data(build_ele)
        pl = g.Polygon3D()
        pl += g.Point3D(0, 20, 0)
        pl += g.Point3D(0, all_data[1] - 20, 0)
        pl += g.Point3D(0, all_data[1], 20)
        pl += g.Point3D(0, all_data[1], all_data[4] - all_data[10])
        pl += g.Point3D(0, 0, all_data[4] - all_data[10])
        pl += g.Point3D(0, 0, 20)
        pl += g.Point3D(0, 20, 0)
 
        dir = g.Polyline3D()
        dir += g.Point3D(0, 20, 0)
        dir += g.Point3D(all_data[8], 20, 0)
        e, f = g.CreatePolyhedron(pl, dir)
        return f
