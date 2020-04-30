import itertools
import time
import pandas as pd
from s_box import S_box
from extended_binary_mask import binary_string, extended_binary_mask, create_delta_set

def create_table(s_box_n_bit, V_n, save=False):
    D_table = dict()
    D_table_alpha = dict()
    for alpha in V_n:
        temp_x_list_alpha = set()
        for beta in V_n:
            temp_x_list = set()
            for i in V_n:
                s_box_result = s_box_n_bit.calculate_result(i)
                s_box_alpha_result = s_box_n_bit.calculate_result(i ^ alpha)
                if s_box_alpha_result == s_box_result ^ beta:
                    temp_x_list.add(i)
            D_table[(alpha, beta)] = temp_x_list
            temp_x_list_alpha.union(temp_x_list)
        D_table_alpha[alpha] = temp_x_list_alpha
    
    TD_table = dict()
    max_DP_table = dict()
    delta_alpha_table = dict()
    delta_beta_table = dict()
    for pair in alpha_beta_pairs:
        delta_alpha = precalculated_delta_set[pair[0]]
        delta_beta = precalculated_delta_set[pair[1]]
        all_diff = itertools.product(delta_alpha, delta_beta)
        temp_x_list = list()
        temp_max_dp = list()
        if delta_alpha and delta_beta:
            possible_x = set()
            for alpha_ in delta_alpha:
                possible_x.union(D_table_alpha[alpha_])
            for x in list(possible_x):
                flag = True
                for alpha_1 in delta_alpha:
                    if (s_box_n_bit.calculate_result(x ^ alpha_1) ^ s_box_n_bit.calculate_result(x)) not in delta_beta:
                        flag = False
                        break
                if flag: 
                    temp_x_list.append(x)
        for differential in all_diff:
                temp_max_dp.append(len(D_table[differential]))
        # print(temp_x_list)
        TD_table[pair] = temp_x_list
        max_DP_table[pair] = max(temp_max_dp) if temp_max_dp else 0
        delta_alpha_table[pair] = delta_alpha
        delta_beta_table[pair] = delta_beta

    result = dict()
    for i in TD_table:
        if len(delta_alpha_table[i]) > 5 and i[1]!='****':
            result[i] = [max_DP_table[i]]
            result[i].append(len(TD_table[i]))
            result[i].append(TD_table[i])
            result[i].append(delta_alpha_table[i])
            result[i].append(delta_beta_table[i])
        
        
    df = pd.DataFrame.from_dict(data=result, orient='index', columns=["maxDP(a', b')", "TDP(a, b)", 'TD(a,b)', 'delta(alpha)', 'delta(beta)'])
    
    if save:
        if s_box_n_bit.name:
            df.to_csv(s_box_n_bit.name + '.csv')
            print('File was saved!')
        else:
            raise Exception('File cannot be saved: no S-box name!')
    return df

# start
mask_elements = ['0', '1', '*']
n = 4
V_n = list(range(2 ** n))

time_start = time.time()
all_masks = [''.join(i) for i in list(itertools.product(mask_elements, repeat=n))]
print('All masks built.')
print("Time: {}".format(time.time() - time_start))

# calculate all possible alpha-beta pairs
time_start = time.time()
alpha_beta_pairs = list(itertools.product(all_masks, repeat=2))
# for alpha in all_masks:
#     for beta in all_masks:
#         alpha_beta_pairs.append(tuple([alpha, beta]))
print('All possible alpha-beta pairs calculated.')
print('Time: {}'.format(time.time() - time_start))

#precalculate delta for each mask
time_start = time.time()
precalculated_delta_set = dict()
for mask in all_masks:
    precalculated_delta_set[mask] = create_delta_set(extended_binary_mask(mask))
print('Delta sets precalculated.')
print('Time: {}'.format(time.time() - time_start))

s_box_dict = {
            #   'kalyna_1': [168, 67, 95, 6, 107, 117, 108, 89, 113, 223, 135, 149, 23, 240, 216, 9, 109, 243, 29, 203, 201, 77, 44, 175, 121, 224, 151, 253, 111, 75, 69, 57, 62, 221, 163, 79, 180, 182, 154, 14, 31, 191, 21, 225, 73, 210, 147, 198, 146, 114, 158, 97, 209, 99, 250, 238, 244, 25, 213, 173, 88, 164, 187, 161, 220, 242, 131, 55, 66, 228, 122, 50, 156, 204, 171, 74, 143, 110, 4, 39, 46, 231, 226, 90, 150, 22, 35, 43, 194, 101, 102, 15, 188, 169, 71, 65, 52, 72, 252, 183, 106, 136, 165, 83, 134, 249, 91, 219, 56, 123, 195, 30, 34, 51, 36, 40, 54, 199, 178, 59, 142, 119, 186, 245, 20, 159, 8, 85, 155, 76, 254, 96, 92, 218, 24, 70, 205, 125, 33, 176, 63, 27, 137, 255, 235, 132, 105, 58, 157, 215, 211, 112, 103, 64, 181, 222, 93, 48, 145, 177, 120, 17, 1, 229, 0, 104, 152, 160, 197, 2, 166, 116, 45, 11, 162, 118, 179, 190, 206, 189, 174, 233, 138, 49, 28, 236, 241, 153, 148, 170, 246, 38, 47, 239, 232, 140, 53, 3, 212, 127, 251, 5, 193, 94, 144, 32, 61, 130, 247, 234, 10, 13, 126, 248, 80, 26, 196, 7, 87, 184, 60, 98, 227, 200, 172, 82, 100, 16, 208, 217, 19, 12, 18, 41, 81, 185, 207, 214, 115, 141, 129, 84, 192, 237, 78, 68, 167, 42, 133, 37, 230, 202, 124, 139, 86, 128]
            #   'kalyna_2': [206, 187, 235, 146, 234, 203, 19, 193, 233, 58, 214, 178, 210, 144, 23, 248, 66, 21, 86, 180, 101, 28, 136, 67, 197, 92, 54, 186, 245, 87, 103, 141, 49, 246, 100, 88, 158, 244, 34, 170, 117, 15, 2, 177, 223, 109, 115, 77, 124, 38, 46, 247, 8, 93, 68, 62, 159, 20, 200, 174, 84, 16, 216, 188, 26, 107, 105, 243, 189, 51, 171, 250, 209, 155, 104, 78, 22, 149, 145, 238, 76, 99, 142, 91, 204, 60, 25, 161, 129, 73, 123, 217, 111, 55, 96, 202, 231, 43, 72, 253, 150, 69, 252, 65, 18, 13, 121, 229, 137, 140, 227, 32, 48, 220, 183, 108, 74, 181, 63, 151, 212, 98, 45, 6, 164, 165, 131, 95, 42, 218, 201, 0, 126, 162, 85, 191, 17, 213, 156, 207, 14, 10, 61, 81, 125, 147, 27, 254, 196, 71, 9, 134, 11, 143, 157, 106, 7, 185, 176, 152, 24, 50, 113, 75, 239, 59, 112, 160, 228, 64, 255, 195, 169, 230, 120, 249, 139, 70, 128, 30, 56, 225, 184, 168, 224, 12, 35, 118, 29, 37, 36, 5, 241, 110, 148, 40, 154, 132, 232, 163, 79, 119, 211, 133, 226, 82, 242, 130, 80, 122, 47, 116, 83, 179, 97, 175, 57, 53, 222, 205, 31, 153, 172, 173, 114, 44, 221, 208, 135, 190, 94, 166, 236, 4, 198, 3, 52, 251, 219, 89, 182, 194, 1, 240, 90, 237, 167, 102, 33, 127, 138, 39, 199, 192, 41, 215],
            #   'kalyna_3': [147, 217, 154, 181, 152, 34, 69, 252, 186, 106, 223, 2, 159, 220, 81, 89, 74, 23, 43, 194, 148, 244, 187, 163, 98, 228, 113, 212, 205, 112, 22, 225, 73, 60, 192, 216, 92, 155, 173, 133, 83, 161, 122, 200, 45, 224, 209, 114, 166, 44, 196, 227, 118, 120, 183, 180, 9, 59, 14, 65, 76, 222, 178, 144, 37, 165, 215, 3, 17, 0, 195, 46, 146, 239, 78, 18, 157, 125, 203, 53, 16, 213, 79, 158, 77, 169, 85, 198, 208, 123, 24, 151, 211, 54, 230, 72, 86, 129, 143, 119, 204, 156, 185, 226, 172, 184, 47, 21, 164, 124, 218, 56, 30, 11, 5, 214, 20, 110, 108, 126, 102, 253, 177, 229, 96, 175, 94, 51, 135, 201, 240, 93, 109, 63, 136, 141, 199, 247, 29, 233, 236, 237, 128, 41, 39, 207, 153, 168, 80, 15, 55, 36, 40, 48, 149, 210, 62, 91, 64, 131, 179, 105, 87, 31, 7, 28, 138, 188, 32, 235, 206, 142, 171, 238, 49, 162, 115, 249, 202, 58, 26, 251, 13, 193, 254, 250, 242, 111, 189, 150, 221, 67, 82, 182, 8, 243, 174, 190, 25, 137, 50, 38, 176, 234, 75, 100, 132, 130, 107, 245, 121, 191, 1, 95, 117, 99, 27, 35, 61, 104, 42, 101, 232, 145, 246, 255, 19, 88, 241, 71, 10, 127, 197, 167, 231, 97, 90, 6, 70, 68, 66, 4, 160, 219, 57, 134, 84, 170, 140, 52, 33, 139, 248, 12, 116, 103],
            #   'kalyna_4': [104, 141, 202, 77, 115, 75, 78, 42, 212, 82, 38, 179, 84, 30, 25, 31, 34, 3, 70, 61, 45, 74, 83, 131, 19, 138, 183, 213, 37, 121, 245, 189, 88, 47, 13, 2, 237, 81, 158, 17, 242, 62, 85, 94, 209, 22, 60, 102, 112, 93, 243, 69, 64, 204, 232, 148, 86, 8, 206, 26, 58, 210, 225, 223, 181, 56, 110, 14, 229, 244, 249, 134, 233, 79, 214, 133, 35, 207, 50, 153, 49, 20, 174, 238, 200, 72, 211, 48, 161, 146, 65, 177, 24, 196, 44, 113, 114, 68, 21, 253, 55, 190, 95, 170, 155, 136, 216, 171, 137, 156, 250, 96, 234, 188, 98, 12, 36, 166, 168, 236, 103, 32, 219, 124, 40, 221, 172, 91, 52, 126, 16, 241, 123, 143, 99, 160, 5, 154, 67, 119, 33, 191, 39, 9, 195, 159, 182, 215, 41, 194, 235, 192, 164, 139, 140, 29, 251, 255, 193, 178, 151, 46, 248, 101, 246, 117, 7, 4, 73, 51, 228, 217, 185, 208, 66, 199, 108, 144, 0, 142, 111, 80, 1, 197, 218, 71, 63, 205, 105, 162, 226, 122, 167, 198, 147, 15, 10, 6, 230, 43, 150, 163, 28, 175, 106, 18, 132, 57, 231, 176, 130, 247, 254, 157, 135, 92, 129, 53, 222, 180, 165, 252, 128, 239, 203, 187, 107, 118, 186, 90, 125, 120, 11, 149, 227, 173, 116, 152, 59, 54, 100, 109, 220, 240, 89, 169, 76, 23, 127, 145, 184, 201, 87, 27, 224, 97],
            #   'kalyna_5': [164, 162, 169, 197, 78, 201, 3, 217, 126, 15, 210, 173, 231, 211, 39, 91, 227, 161, 232, 230, 124, 42, 85, 12, 134, 57, 215, 141, 184, 18, 111, 40, 205, 138, 112, 86, 114, 249, 191, 79, 115, 233, 247, 87, 22, 172, 80, 192, 157, 183, 71, 113, 96, 196, 116, 67, 108, 31, 147, 119, 220, 206, 32, 140, 153, 95, 68, 1, 245, 30, 135, 94, 97, 44, 75, 29, 129, 21, 244, 35, 214, 234, 225, 103, 241, 127, 254, 218, 60, 7, 83, 106, 132, 156, 203, 2, 131, 51, 221, 53, 226, 89, 90, 152, 165, 146, 100, 4, 6, 16, 77, 28, 151, 8, 49, 238, 171, 5, 175, 121, 160, 24, 70, 109, 252, 137, 212, 199, 255, 240, 207, 66, 145, 248, 104, 10, 101, 142, 182, 253, 195, 239, 120, 76, 204, 158, 48, 46, 188, 11, 84, 26, 166, 187, 38, 128, 72, 148, 50, 125, 167, 63, 174, 34, 61, 102, 170, 246, 0, 93, 189, 74, 224, 59, 180, 23, 139, 159, 118, 176, 36, 154, 37, 99, 219, 235, 122, 62, 92, 179, 177, 41, 242, 202, 88, 110, 216, 168, 47, 117, 223, 20, 251, 19, 73, 136, 178, 236, 228, 52, 45, 150, 198, 58, 237, 149, 14, 229, 133, 107, 64, 33, 155, 9, 25, 43, 82, 222, 69, 163, 250, 81, 194, 181, 209, 144, 185, 243, 55, 193, 13, 186, 65, 17, 56, 123, 190, 208, 213, 105, 54, 200, 98, 27, 130, 143],
            #   'kalyna_6': [131, 242, 42, 235, 233, 191, 123, 156, 52, 150, 141, 152, 185, 105, 140, 41, 61, 136, 104, 6, 57, 17, 76, 14, 160, 86, 64, 146, 21, 188, 179, 220, 111, 248, 38, 186, 190, 189, 49, 251, 195, 254, 128, 97, 225, 122, 50, 210, 112, 32, 161, 69, 236, 217, 26, 93, 180, 216, 9, 165, 85, 142, 55, 118, 169, 103, 16, 23, 54, 101, 177, 149, 98, 89, 116, 163, 80, 47, 75, 200, 208, 143, 205, 212, 60, 134, 18, 29, 35, 239, 244, 83, 25, 53, 230, 127, 94, 214, 121, 81, 34, 20, 247, 30, 74, 66, 155, 65, 115, 45, 193, 92, 166, 162, 224, 46, 211, 40, 187, 201, 174, 106, 209, 90, 48, 144, 132, 249, 178, 88, 207, 126, 197, 203, 151, 228, 22, 108, 250, 176, 109, 31, 82, 153, 13, 78, 3, 145, 194, 77, 100, 119, 159, 221, 196, 73, 138, 154, 36, 56, 167, 87, 133, 199, 124, 125, 231, 246, 183, 172, 39, 70, 222, 223, 59, 215, 158, 43, 11, 213, 19, 117, 240, 114, 182, 157, 27, 1, 63, 68, 229, 135, 253, 7, 241, 171, 148, 24, 234, 252, 58, 130, 95, 5, 84, 219, 0, 139, 227, 72, 12, 202, 120, 137, 10, 255, 62, 91, 129, 238, 113, 226, 218, 44, 184, 181, 204, 110, 168, 107, 173, 96, 198, 8, 4, 2, 232, 245, 79, 164, 243, 192, 206, 67, 37, 28, 33, 51, 15, 175, 71, 237, 102, 99, 147, 170],
            #   'kalyna_7': [69, 212, 11, 67, 241, 114, 237, 164, 194, 56, 230, 113, 253, 182, 58, 149, 80, 68, 75, 226, 116, 107, 30, 17, 90, 198, 180, 216, 165, 138, 112, 163, 168, 250, 5, 217, 151, 64, 201, 144, 152, 143, 220, 18, 49, 44, 71, 106, 153, 174, 200, 127, 249, 79, 93, 150, 111, 244, 179, 57, 33, 218, 156, 133, 158, 59, 240, 191, 239, 6, 238, 229, 95, 32, 16, 204, 60, 84, 74, 82, 148, 14, 192, 40, 246, 86, 96, 162, 227, 15, 236, 157, 36, 131, 126, 213, 124, 235, 24, 215, 205, 221, 120, 255, 219, 161, 9, 208, 118, 132, 117, 187, 29, 26, 47, 176, 254, 214, 52, 99, 53, 210, 42, 89, 109, 77, 119, 231, 142, 97, 207, 159, 206, 39, 245, 128, 134, 199, 166, 251, 248, 135, 171, 98, 63, 223, 72, 0, 20, 154, 189, 91, 4, 146, 2, 37, 101, 76, 83, 12, 242, 41, 175, 23, 108, 65, 48, 233, 147, 85, 247, 172, 104, 38, 196, 125, 202, 122, 62, 160, 55, 3, 193, 54, 105, 102, 8, 22, 167, 188, 197, 211, 34, 183, 19, 70, 50, 232, 87, 136, 43, 129, 178, 78, 100, 28, 170, 145, 88, 46, 155, 92, 27, 81, 115, 66, 35, 1, 110, 243, 13, 190, 61, 10, 45, 31, 103, 51, 25, 123, 94, 234, 222, 139, 203, 169, 140, 141, 173, 73, 130, 228, 186, 195, 21, 209, 224, 137, 252, 177, 185, 181, 7, 121, 184, 225],
            #   'kalyna_8': [178, 182, 35, 17, 167, 136, 197, 166, 57, 143, 196, 232, 115, 34, 67, 195, 130, 39, 205, 24, 81, 98, 45, 247, 92, 14, 59, 253, 202, 155, 13, 15, 121, 140, 16, 76, 116, 28, 10, 142, 124, 148, 7, 199, 94, 20, 161, 33, 87, 80, 78, 169, 128, 217, 239, 100, 65, 207, 60, 238, 46, 19, 41, 186, 52, 90, 174, 138, 97, 51, 18, 185, 85, 168, 21, 5, 246, 3, 6, 73, 181, 37, 9, 22, 12, 42, 56, 252, 32, 244, 229, 127, 215, 49, 43, 102, 111, 255, 114, 134, 240, 163, 47, 120, 0, 188, 204, 226, 176, 241, 66, 180, 48, 95, 96, 4, 236, 165, 227, 139, 231, 29, 191, 132, 123, 230, 129, 248, 222, 216, 210, 23, 206, 75, 71, 214, 105, 108, 25, 153, 154, 1, 179, 133, 177, 249, 89, 194, 55, 233, 200, 160, 237, 79, 137, 104, 109, 213, 38, 145, 135, 88, 189, 201, 152, 220, 117, 192, 118, 245, 103, 107, 126, 235, 82, 203, 209, 91, 159, 11, 219, 64, 146, 26, 250, 172, 228, 225, 113, 31, 101, 141, 151, 158, 149, 144, 93, 183, 193, 175, 84, 251, 2, 224, 53, 187, 58, 77, 173, 44, 61, 86, 8, 27, 74, 147, 106, 171, 184, 122, 242, 125, 218, 63, 254, 62, 190, 234, 170, 68, 198, 208, 54, 72, 112, 150, 119, 36, 83, 223, 243, 131, 40, 50, 69, 30, 164, 211, 162, 70, 110, 156, 221, 99, 212, 157]
              'k1': [7, 9, 4, 13, 0, 2, 12, 11, 10, 8, 1, 6, 14, 5, 15, 3]
            #   'k2': [1, 9, 6, 5, 11, 14, 2, 8, 4, 10, 15, 3, 0, 7, 12, 13],
            #   'k3': [10, 12, 3, 8, 11, 7, 13, 0, 4, 5, 1, 15, 14, 9, 6, 2],
            #   'k4': [14, 10, 15, 1, 0, 13, 7, 4, 5, 2, 8, 6, 3, 11, 9, 12],
            #   'k5': [11, 0, 13, 14, 6, 4, 7, 9, 5, 1, 12, 2, 8, 15, 10, 3],
            #   'k6': [1, 12, 3, 8, 0, 6, 14, 13, 15, 11, 4, 5, 9, 2, 10, 7],
            #   'k7': [14, 7, 11, 13, 8, 2, 5, 6, 3, 0, 1, 12, 15, 9, 4, 10],
            #   'k8': [4, 3, 10, 11, 13, 14, 8, 5, 9, 1, 7, 12, 15, 2, 6, 0],
            #   'xor_5': [5, 4, 7, 6, 1, 0, 3, 2, 13, 12, 15, 14, 9, 8, 11, 10],
            #   'xor_7': [7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8],
            #   'xor_11': [11, 10, 9, 8, 15, 14, 13, 12, 3, 2, 1, 0, 7, 6, 5, 4],
            #   'shift_left_2': [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15],
            #   'shift_left_3': [0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15]
            }

for s_box_name in s_box_dict:
    time_start = time.time()
    curent_s_box = S_box(n, name=s_box_name, s_box=s_box_dict[s_box_name])
    a = create_table(curent_s_box, V_n, save=True)
    print('Time: {}'.format(time.time() - time_start))
    # for i in a:
    #     if a[i]:
            # print(i, '---', a[i])
