LatticePointIndicator[x_, y_] := Module[{},
  If[x == 0 && y == 0, Return[False]];
  If[Abs[x] == 1 || Abs[y] == 1, Return[False]];
  If[x == 0, Return[Abs[y] > 1]];
  If[y == 0, Return[Abs[x] > 1]];
  Return[GCD[Abs[x], Abs[y]] > 1]
];

GeneraGriglia2D[raggio_] := Module[{matrice, dim},
  dim = raggio;
  matrice = Table[
    If[LatticePointIndicator[x, y], 1, 0], 
    {y, -dim, dim}, {x, -dim, dim}
  ];
  
  MatrixPlot[matrice,
    ColorRules -> {1 -> Black, 0 -> White},
    Frame -> True,
    FrameTicks -> Automatic,
    GridLines -> {Automatic, Automatic},
    GridLinesStyle -> Directive[GrayLevel[0.9]],
    PlotLabel -> Style["Il Setaccio Geometrico di Enrico (2D)", 14, Bold],
    Epilog -> {
      Directive[Red, Thick, Dashed], 
      Line[{{0, 0}, {2 dim + 2, 2 dim + 2}}],
      Line[{{0, 2 dim + 2}, {2 dim + 2, 0}}],
      Directive[GrayLevel[0.3], Thick],
      Line[{{dim + 1, 0}, {dim + 1, 2 dim + 2}}],
      Line[{{0, dim + 1}, {2 dim + 2, dim + 1}}]
    }
  ]
];

GeneraGriglia2D[30]
