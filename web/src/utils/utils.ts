export interface Point {
    x: number,
    y: number,
}

function _unpackLogBin(data): Point[] {
    let points = [];
    let x = new DataView(data);
    for (var i = 0; i < data.byteLength; i += 6) {
        points.push({ x: x.getUint32(i, false) * 1000, y: x.getUint16(i + 4, false) });
    }
    return points;
}

export async function loadData(url: string): Promise<Point[]> {
    return fetch(url)
        .then(response => response.arrayBuffer())
        .then(data => _unpackLogBin(data));
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