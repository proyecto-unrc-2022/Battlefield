{- generate only permutations which x+iésim is a perfect square -}

perms :: Eq a => [a] -> [[a]]
perms [] = [[]]
perms xs = [x:ps | x <- xs, ps <- perms (delete x xs),]



delete :: Eq a => a -> [a] -> [a]
delete x [] = []
delete x (y:ys) | x == y = ys
                | otherwise = y : delete x ys


isSquare :: Int -> Bool
isSquare n = (floor . sqrt . fromIntegral) n == (ceiling . sqrt . fromIntegral) n

