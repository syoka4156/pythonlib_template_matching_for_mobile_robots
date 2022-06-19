import cv2
import numpy as np


class ImageProcessing:
    """
    カメラの画像を使用して画像処理を行うクラス
    """

    def __init__(self, camera_img, dir_path="./data"):
        """
        Args:
            camera_img (numpy.ndarray): カメラ画像
            dir_path (str): テンプレート画像が入っているディレクトリパス
        """

        self._prepare_camera_image(camera_img)
        self._prepare_template(dir_path)

    def _prepare_camera_image(self, camera_img):
        self.camera_gray_img = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)
        self.camera_height, self.camera_width = camera_img.shape[0:2]

    def _prepare_template(self, dir_path):
        template1_img = cv2.imread(dir_path + "/template1_in_square.png", 0)
        template2_img = cv2.imread(dir_path + "/template2_in_square.png", 0)
        self.template_height, self.template_width = template1_img.shape[0:2]

        self.template_list = [template1_img, template2_img]
        self.template_name_list = ["template1", "template2"]
        self.template_result_list = [-1, -1]

    def template_matching(self, min_area=1000, min_ccoeff=0):
        """
        矩形を検出し，矩形内の画像でテンプレートマッチングを行う関数

        Args:
            min_area (int):
                検出する矩形の最小面積 (1以上)
            min_ccoeff (int):
                有効な最小の一致係数 [-1, 1] (大きいほど一致している)

        Returns:
            str: 最も一致したテンプレートの名前
        """

        contour_list = self._create_contour_list()
        self.camera_gray_img = cv2.threshold(
            self.camera_gray_img, 100, 255, cv2.THRESH_BINARY
        )[1]

        for target_contour in contour_list:
            if cv2.contourArea(target_contour) > min_area:
                arclen = cv2.arcLength(target_contour, True)
                vertex_arr = np.float32(
                    cv2.approxPolyDP(target_contour, 0.01 * arclen, True)
                )

                if len(vertex_arr) == 4:
                    if vertex_arr[1][0][0] < vertex_arr[3][0][0]:
                        trans_vertex_arr = np.float32(
                            [
                                [0, 0],
                                [0, self.template_width],
                                [self.template_height, self.template_width],
                                [self.template_height, 0],
                            ]
                        )
                    else:
                        trans_vertex_arr = np.float32(
                            [
                                [0, 0],
                                [self.template_height, 0],
                                [self.template_height, self.template_width],
                                [0, self.template_width],
                            ]
                        )

                    perspective_matrix = cv2.getPerspectiveTransform(
                        vertex_arr, trans_vertex_arr
                    )
                    inside_img = cv2.warpPerspective(
                        self.camera_gray_img,
                        perspective_matrix,
                        (self.template_width, self.template_height),
                    )

                    for idx, template in enumerate(self.template_list):
                        ccoeff = cv2.matchTemplate(
                            inside_img, template, cv2.TM_CCOEFF_NORMED
                        )

                        if ccoeff[0][0] > self.template_result_list[idx]:
                            self.template_result_list[idx] = ccoeff[0][0]

        max_index = np.argmax(self.template_result_list)
        if self.template_result_list[max_index] < min_ccoeff:
            return "nothing"
        else:
            return self.template_name_list[max_index]

    def _create_contour_list(self):
        camera_edge_img = cv2.Canny(self.camera_gray_img, 200, 200)
        contour_list = cv2.findContours(
            camera_edge_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )[0]

        return contour_list
