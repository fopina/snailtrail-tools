export interface Point {
  x: number
  y: number
}

function _unpackLogBin (data): Point[] {
  const points = []
  const x = new DataView(data)
  for (let i = 0; i < data.byteLength; i += 6) {
    points.push({ x: x.getUint32(i, false) * 1000, y: x.getUint16(i + 4, false) })
  }
  return points
}

export async function loadData (url: string): Promise<Point[]> {
  return await fetch(url)
    .then(async response => await response.arrayBuffer())
    .then(data => _unpackLogBin(data))
}

/*

    document.getElementById('startDate').addEventListener('change', function() {
      _dateRangeChanged();
    });
    document.getElementById('endDate').addEventListener('change', function() {
      _dateRangeChanged();
    });
  })
*/
