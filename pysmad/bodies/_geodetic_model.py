from pathlib import Path


class GeodeticModel:

    GEO_FILE_MU_LINE = 4
    GEO_FILE_RADIUS_LINE = 5
    GEO_FILE_FLATTENING_LINE = 6
    GEO_FILE_VAR_INDEX = 18
    GEO_FILE_VAR_LENGTH = 20
    GEO_FILE_C_START = 17
    GEO_FILE_S_START = 37
    GEO_FILE_DEG_INDEX = 7
    GEO_FILE_ORDER_INDEX = 12
    GEO_FILE_DEG_ORDER_LENGTH = 3
    GEO_FILE_COEFFICIENT_LINE_START = 13
    DEFAULT_DEGREE = 18

    def __init__(self, model_path: Path) -> None:
        self.c_coefficients: list[list[float]]
        self.s_coefficients: list[list[float]]
        self.mu: float
        self.radius: float
        self.flattening: float
        self.update_from_file(model_path)

    def update_from_file(self, file_path: Path) -> None:
        with open(file_path, "r") as f:
            lines = f.readlines()

        # get mu
        mu_line = lines[GeodeticModel.GEO_FILE_MU_LINE]
        mu_str = mu_line[
            GeodeticModel.GEO_FILE_VAR_INDEX : GeodeticModel.GEO_FILE_VAR_INDEX + GeodeticModel.GEO_FILE_VAR_LENGTH
        ]
        self.mu = float(mu_str)

        # get equatorial radius
        r_line = lines[GeodeticModel.GEO_FILE_RADIUS_LINE]
        r_str = r_line[
            GeodeticModel.GEO_FILE_VAR_INDEX : GeodeticModel.GEO_FILE_VAR_INDEX + GeodeticModel.GEO_FILE_VAR_LENGTH
        ]
        self.radius = float(r_str)

        # get flattening
        f_line = lines[GeodeticModel.GEO_FILE_FLATTENING_LINE]
        f_str = f_line[
            GeodeticModel.GEO_FILE_VAR_INDEX : GeodeticModel.GEO_FILE_VAR_INDEX + GeodeticModel.GEO_FILE_VAR_LENGTH
        ]
        self.flattening = float(f_str)

        # get c and s coefficients
        self.c_coefficients = [[1], [0, 0]]
        self.s_coefficients = [[0], [0, 0]]
        for line in lines[GeodeticModel.GEO_FILE_COEFFICIENT_LINE_START :]:

            # get degree of current line
            deg_idx_start = GeodeticModel.GEO_FILE_DEG_INDEX
            deg_idx_end = deg_idx_start + GeodeticModel.GEO_FILE_DEG_ORDER_LENGTH
            deg = int(line[deg_idx_start:deg_idx_end])

            # get order of current line
            order_idx_start = GeodeticModel.GEO_FILE_ORDER_INDEX
            order_idx_end = order_idx_start + GeodeticModel.GEO_FILE_DEG_ORDER_LENGTH
            order = int(line[order_idx_start:order_idx_end])

            # get c coefficient
            c_idx_start = GeodeticModel.GEO_FILE_C_START
            c_idx_end = c_idx_start + GeodeticModel.GEO_FILE_VAR_LENGTH
            c_str = line[c_idx_start:c_idx_end]
            c = float(c_str)

            # get s coefficient
            s_idx_start = GeodeticModel.GEO_FILE_S_START
            s_idx_end = s_idx_start + GeodeticModel.GEO_FILE_VAR_LENGTH
            s_str = line[s_idx_start:s_idx_end]
            s = float(s_str)

            # end if max degree or order reached
            if deg > GeodeticModel.DEFAULT_DEGREE or order > GeodeticModel.DEFAULT_DEGREE:
                break

            # add new list if new degree found
            elif deg == len(self.c_coefficients):
                self.c_coefficients.append([c])
                self.s_coefficients.append([s])

            # append to existing list if same degree
            else:
                self.c_coefficients[deg].append(c)
                self.s_coefficients[deg].append(s)
