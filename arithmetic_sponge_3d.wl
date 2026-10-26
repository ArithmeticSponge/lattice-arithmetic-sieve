LatticePointIndicator3D[i_, j_, k_] := If[
   (i == 0 && j == 0 && k == 0) || Abs[i] == 1 || Abs[j] == 1 || Abs[k] == 1, 
   False, 
   GCD[GCD[Abs[i], Abs[j]], Abs[k]] > 1
];

GeneraSpugna3D[dim_] := Module[{punti},
  punti = Flatten[
    Table[
      If[LatticePointIndicator3D[i, j, k], {i, j, k}, Nothing], 
      {i, -dim, dim}, {j, -dim, dim}, {k, -dim, dim}
    ], 
    2
  ];
  
  Graphics3D[{PointSize[0.015], Black, Point[punti]}, 
   Boxed -> True, 
   Axes -> True, 
   AxesLabel -> {"Asse X", "Asse Y", "Asse Z"}, 
   PlotLabel -> Style["La Spugna Aritmetica 3D di Enrico", 14, Bold], 
   ImageSize -> Medium]
];

GeneraSpugna3D
