// Change these numbers to define the axes of the graph
const axisDefinitions = {
    x: {
      min: -10,
      max: 10,
      majorUnit: 5,
      minorUnit: 1,
      label: 'x'
    },
    y: {
      min: -10,
      max: 10,
      majorUnit: 5,
      minorUnit: 1,
      label: 'y'
    }
  };
  
  const displayOptions = {
    xAxisMargin: axisDefinitions.x.minorUnit,
    yAxisMargin: axisDefinitions.y.minorUnit,
    majorTickGridlines: true,
  }
  
  // To see examples, uncomment the commented lines below
  
  // Add the functions that you want to plot here
  // Functions are in the form x => f(x)
  // Optionally, the function can be restricted to a domain using [function, start, end]
  
  
  const functions = [
    // [x => Math.sin(x), -2 * Math.PI, 2 * Math.PI]
    [x => x ** 2, -30, 30],
    [x => x ** 2 + 2, -30, 30, '#7547d8'],
    [x => x ** 2 - 2, -30, 30, '#f4b42e'],
  ];
  
  const shadedRegion = {
    // upperBound: x => Math.exp(x),
    // lowerBound: x => Math.sin(x),
    // leftBound: -2 * Math.PI,
    // rightBound: 2 * Math.PI
  };
  
  // Lines are in the form [[x1, y1], [x2, y2], extends from start, extends from end, dashed]
  const lines = [
    // [[-1, 0], [0, 1], true, false, true]
  ];
  
  // Points are in the form [x, y, hollow, label]
  const points = [
    [-2 * Math.PI, 0, false, 'A'],
    [0, 1, true],
    [2 * Math.PI, 0, false, 'Bbbbb']
  ];
  
  // Text doesn't work right now
  // // Text is in the form [x, y, text]. Use '\\[ \\]' to make LaTeX
  // const texts = [
  //   [-3, 5, () => '\\[y = e^x\\]'],
  //   [-4, -1, () =>'\\[y = \\sin(x)\\]']
  // ]
  
  // Don't touch anything after this if you don't know what you're doing
  const axisColor = '#424548';
  const backgroundColor = '#0875BE';
  const foregroundColor = '#1ABC9C';
  const lineColor = '#7547D8';
  const closedPointColor = '#34495E';
  const openPointColor = '#FFFFFF';
  JXG.Options.layer.axis = 6;
  JXG.Options.layer.ticks = 6;
  JXG.Options.text.cssDefaultStyle = 'font-family: Symbola;';
  JXG.Options.text.display = 'internal';
  JXG.Options.text.highlightCssDefaultStyle = '';
  // JXG.Options.text.useMathJax = true;
  const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [
      axisDefinitions.x.min - displayOptions.xAxisMargin,
      axisDefinitions.y.max + displayOptions.yAxisMargin,
      axisDefinitions.x.max + displayOptions.xAxisMargin,
      axisDefinitions.y.min - displayOptions.yAxisMargin
    ],
    axis: false,
    grid: false,
    showNavigation: false,
    showCopyright: false
  });
  board.renderer.type = 'svg';
  // MathJax.Hub.Config({ jax: ['input/TeX', 'output/SVG'] });
  const xAxis = board.create('axis', [[0, 0], [1, 0]], {
    label: {
      anchorX: 'right',
      cssStyle: 'font-family: "Times New Roman"; font-style: italic',
      offset: [-10, 10],
      position: 'rt'
    },
    name: axisDefinitions.x.label,
    strokeColor: axisColor,
    ticks: {
      insertTicks: false,
      label: {
        anchorX: 'middle',
        offset: [0, -10]
      },
      majorHeight: displayOptions.majorTickGridlines ? -1 : 20,
      minorTicks: axisDefinitions.x.majorUnit / axisDefinitions.x.minorUnit - 1,
      strokeColor: axisColor,
      ticksDistance: axisDefinitions.x.majorUnit
    },
    withLabel: true
  });
  const yAxis = board.create('axis', [[0, 1], [0, 0]], {
    label: {
      cssStyle: 'font-family: "Times New Roman"; font-style: italic',
      offset: [10, -10],
      position: 'lft'
    },
    name: axisDefinitions.y.label,
    strokeColor: axisColor,
    ticks: {
      insertTicks: false,
      label: {
        anchorX: 'right',
        offset: [-10, 0]
      },
      majorHeight: displayOptions.majorTickGridlines ? -1 : 20,
      minorTicks: axisDefinitions.y.majorUnit / axisDefinitions.y.minorUnit - 1,
      strokeColor: axisColor,
      ticksDistance: axisDefinitions.y.majorUnit
    },
    withLabel: true
  });
  xAxis.setArrow(false, false);
  yAxis.setArrow(false, false);
  const xArrows = board.create(
    'axis',
    [
      [axisDefinitions.x.min - 1, 0],
      [axisDefinitions.x.max + 1, 0]
    ],
    {
      strokeColor: axisColor,
      ticks: { visible: false }
    }
  );
  const yArrows = board.create(
    'axis',
    [[0, axisDefinitions.y.min - 1], [0, axisDefinitions.y.max + 1]],
    {
      strokeColor: axisColor,
      ticks: { visible: false }
    }
  );
  xArrows.setArrow({ type: 1, size: 10 }, { type: 1, size: 10 });
  yArrows.setArrow({ type: 1, size: 10 }, { type: 1, size: 10 });
  if (shadedRegion.upperBound) {
    board.create(
      'inequality',
      [
        board.create(
          'functiongraph',
          [
            shadedRegion.upperBound,
            shadedRegion.leftBound,
            shadedRegion.rightBound
          ],
          {
            strokeWidth: 0
          }
        )
      ],
      { fillColor: foregroundColor }
    );
    if (shadedRegion.lowerBound) {
      board.create(
        'inequality',
        [
          board.create('functiongraph', [shadedRegion.lowerBound], {
            strokeWidth: 0
          })
        ],
        {
          fillColor: '#FFFFFF',
          fillOpacity: '1'
        }
      );
    }
  } else if (shadedRegion.lowerBound) {
    board.create(
      'inequality',
      [
        board.create(
          'functiongraph',
          [
            shadedRegion.lowerBound,
            shadedRegion.leftBound,
            shadedRegion.rightBound
          ],
          {
            strokeWidth: 0
          }
        )
      ],
      { fillColor: foregroundColor, inverse: true }
    );
  }
  functions.forEach(f => {
    board.create('functiongraph', f, {
      strokecolor: f[3] || foregroundColor,
      strokeWidth: 3
    });
  });
  lines.forEach(l => {
    board.create('line', [l[0], l[1]], {
      dash: l[4] ? 2 : 0,
      straightFirst: l[3],
      straightLast: l[2],
      strokecolor: lineColor,
      strokeWidth: 3
    });
  });
  points.forEach(p => {
    let point = board.create('point', [p[0], p[1]], {
      fillColor: p[2] ? openPointColor : closedPointColor,
      name: '',
      strokeColor: closedPointColor
    });
    if (p[3]) {
      point.setLabel(p[3]);
    }
  });
  // texts.forEach(text => {
  //   board.create('text', text, { fontsize: 16 });
  // });
  const svg = new XMLSerializer().serializeToString(board.renderer.svgRoot);
  const textArea = document.getElementById('textarea');
  textArea.value = svg;
  document.getElementById('copy').addEventListener('click', event => {
    textArea.select();
    document.execCommand('copy');
  });
  