LatticePointIndicator[x_, y_] := If[
   (x == 0 && y == 0) || Abs[x] == 1 || Abs[y] == 1, 
   False, 
   If[x == 0, Abs[y] > 1, If[y == 0, Abs[x] > 1, GCD[Abs[x], Abs[y]] > 1]]
];

VisualizzaPrimiENAC[limiteX_] := Module[{conteggioDivisori, record, primi, nac, griglia, lineePrimi, lineeNac, lineeTotali},
  conteggioDivisori = Table[Length[Divisors[x]], {x, 1, limiteX}];
  primi = Select[Range[limiteX], conteggioDivisori[[#]] == 2 &];
  
  record = 0;
  nac = Reap[
    Do[
      If[conteggioDivisori[[x]] > record, 
        record = conteggioDivisori[[x]]; 
        Sow[x]
      ], 
      {x, 1, limiteX}
    ]
  ][];
  nac = If[nac == {}, {}, nac[]];
  
  griglia = Table[
    If[LatticePointIndicator[x, y], 1, 0], 
    {y, 1, 40}, {x, 1, limiteX}
  ];
  
  lineePrimi = {#, Directive[Darker[Green], Thickness[0.008], Opacity[0.35]]} & /@ primi;
  lineeNac = {#, Directive[Orange, Thickness[0.018], Opacity[0.7]]} & /@ nac;
  lineeTotali = Join[lineePrimi, lineeNac];
  
  MatrixPlot[griglia,
    ColorRules -> {1 -> Black, 0 -> White},
    AspectRatio -> 1/3,
    PlotLabel -> Style["Lame di Luce (Verde) e Pilastri Dorati NAC (Arancione)", 14, Bold],
    GridLines -> {lineeTotali, None},
    Frame -> True
  ]
];

VisualizzaPrimiENAC
