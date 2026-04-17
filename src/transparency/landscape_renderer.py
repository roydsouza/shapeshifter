class LandscapeRenderer:
    def render(self, variants_data):
        """
        variants_data: list of dicts with keys: 'id', 'fitness', 'speed', 'tests', 'gas'
        """
        header = "Variant  | Fitness | Speed  | Tests  | Gas Used"
        sep    = "---------|---------|--------|--------|----------"
        print(header)
        print(sep)
        for d in variants_data:
            vid = str(d['id']).ljust(8)
            fit = str(round(d['fitness'], 2)).ljust(7)
            spd = (str(round(d['speed'], 2)) + "x").ljust(6)
            tst = str(d['tests']).ljust(6)
            gas = str(d['gas']).ljust(8)
            print(f"{vid} | {fit} | {spd} | {tst} | {gas}")
