# Phần này sẽ để báo cáo kết quả thử nghiệm của các từng thuật toán
## Format 
- Nêu hàm heuristic sử dụng 
- Kết quả thu được, nêu rõ tham số sử dụng (depth, hàm/engine đem ra so sánh, số ván chơi)
- Giải thích kết quả + show code/hình ảnh minh họa  

**1. Minimax Algorithm**
- Heuristic 1: Coin Party: Khá phế; ở nước tầm 55,56 nó có mobility thấp nên phải pass qua 2 lần. Dù ban đầu có lợi thế tạm thời nhưng lại để đối thủ chiếm corner và các ô quan trọng => mất hết 4 corner => thua 18-46

- Heuristic 2: Local Maximization (basically add weight for each cell)
![Example Image](result/heuristic2_firstTry.jpg)

- Heuristic 3: coinParty + mobility: khá lạ khi có 1 lần bị pass liên tiếp 2 lượt (???) và đi một số nước khá loudy

![Ex2](result/mobility_coinparty_ex.jpg)
![Ex3](result/mobility_coinparty_ex2.jpg)
![have_to_pass](result/have_to_pass.jpg)

Kết quả cuối cùng như cc :) 
![final_res_mobility](final_res_mobility.png)
