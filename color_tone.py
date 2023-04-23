from PIL import Image
import numpy as np


def get_color_tone(color, ratio):
    if color == (0, 0, 255):
        color = "mavi"
    elif color == (255, 0, 0):
        color = "kırmızı"
    elif color == (0, 255, 0):
        color = "yeşil"
    elif color == (255, 255, 0):
        color = "sarı"

    if color == 'mavi':
        color_tones = [
            (230, 230, 255),
            (204, 204, 255),
            (179, 179, 255),
            (153, 153, 255),
            (128, 128, 255),
            (102, 102, 255),
            (77, 77, 255),
            (51, 51, 255),
            (26, 26, 255),
            (0, 0, 255)
        ]
    elif color == 'kırmızı':
        color_tones = [
            (255, 230, 230),
            (255, 204, 204),
            (255, 179, 179),
            (255, 153, 153),
            (255, 128, 128),
            (255, 102, 102),
            (255, 77, 77),
            (255, 51, 51),
            (255, 26, 26),
            (255, 0, 0)
        ]
    elif color == 'yeşil':
        color_tones = [
            (230, 255, 230),
            (204, 255, 204),
            (179, 255, 179),
            (153, 255, 153),
            (128, 255, 128),
            (102, 255, 102),
            (77, 255, 77),
            (51, 255, 51),
            (26, 255, 26),
            (0, 255, 0)
        ]
    elif color == 'sarı':
        color_tones = [
            (255, 255, 230),
            (255, 255, 204),
            (255, 255, 179),
            (255, 255, 153),
            (255, 255, 128),
            (255, 255, 102),
            (255, 255, 77),
            (255, 255, 51),
            (255, 255, 26),
            (255, 255, 0)
        ]

    index = round(ratio * 10) - 1

    return color_tones[index]


def create_gradient_image(colors, ratios, width, height, output_filename):
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    tones_ratios = [(get_color_tone(color, ratio), ratio) for color, ratio in zip(colors, ratios) if ratio > 0]

    sorted_tones_ratios = sorted(tones_ratios, key=lambda x: x[1], reverse=True)

    total_ratio = sum(ratio for _, ratio in sorted_tones_ratios)
    adjusted_ratios = [ratio / total_ratio for _, ratio in sorted_tones_ratios]

    cumulative_ratios = [0] + [sum(adjusted_ratios[:i+1]) for i in range(len(adjusted_ratios))]
    cumulative_ratios[-1] = 1.0

    for x in range(width):
        for y in range(height):
            ratio_index = x / width

            if total_ratio == 1 and len(sorted_tones_ratios) == 1:
                color_name = sorted_tones_ratios[0][0]
                color_start = np.array(get_color_tone(color_name, 1))
                color_end = np.array(get_color_tone(color_name, 0.1))

                t = ratio_index
                current_color = (1 - t) * color_start + t * color_end
                pixels[x, y] = tuple(current_color.astype(int))
            else:
                for i in range(len(cumulative_ratios) - 1):
                    if cumulative_ratios[i] <= ratio_index < cumulative_ratios[i+1]:
                        color_start = np.array(sorted_tones_ratios[i][0])
                        color_end = np.array(sorted_tones_ratios[min(i+1, len(sorted_tones_ratios)-1)][0])

                        t = (ratio_index - cumulative_ratios[i]) / (cumulative_ratios[i+1] - cumulative_ratios[i])
                        current_color = (1 - t) * color_start + t * color_end

                        pixels[x, y] = tuple(current_color.astype(int))
                        break

    img.save(output_filename)


if __name__ == '__main__':
    colors = ['mavi', 'kırmızı', 'yeşil', 'sarı']

    ratios_1 = [0.2, 0, 0, 0.9]  # %87 Mavi, %13 Kırmızı
    ratios_2 = [0.47, 0.2, 0.2, 0]  # %47 Mavi, %20 Yeşil, %20 Sarı, %13 Kırmızı
    ratios_3 = [1, 0, 0, 0]  # %100 Mavi
    ratios_4 = [0, 1, 0, 0]  # %100 Kırmızı
    ratios_5 = [0, 0, 1, 0]  # %100 Yeşil
    ratios_6 = [0, 0, 0, 1]  # %100 Sarı
    create_gradient_image(colors, ratios_1, 1200, 300, 'predefined_gradient_ratios_1.png')
    create_gradient_image(colors, ratios_2, 1200, 300, 'predefined_gradient_ratios_2.png')
    create_gradient_image(colors, ratios_3, 1200, 300, 'predefined_gradient_ratios_3.png')
    create_gradient_image(colors, ratios_4, 1200, 300, 'predefined_gradient_ratios_4.png')
    create_gradient_image(colors, ratios_5, 1200, 300, 'predefined_gradient_ratios_5.png')
    create_gradient_image(colors, ratios_6, 1200, 300, 'predefined_gradient_ratios_6.png')
