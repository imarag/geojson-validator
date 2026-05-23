export const geojsonSamples = [
  {
    title: "Polygon With Geometry & Type Errors",
    description:
      "Polygon with non-numeric coordinate, wrong bbox length, foreign keys, and invalid property types.",
    geojson: `{
  "type": "FeatureCollection",
  "crs": {
    "type": "name",
    "properties": {
      "name": "EPSG:4326"
    }
  },
  "features": [
    {
      "type": "Feature",
      "id": "abc-123",
      "bbox": [0, 0, 10, 10, 20],
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [0, 0],
            [10, 0],
            [10, "5"],
            [5, 10],
            [0, 0]
          ]
        ]
      },
      "properties": {
        "name": null,
        "active": "true",
        "elevation": "200m"
      },
      "unexpected_field": "not allowed"
    }
  ]
}`,
  },

  {
    title: "LineString With Mixed Dimensions",
    description:
      "LineString mixing 2D and 3D coordinates and invalid geometry type casing.",
    geojson: `{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "linestring",
        "coordinates": [
          [102.0, 0.0],
          [103.0, 1.0, 50],
          [104.0]
        ]
      },
      "properties": {
        "description": "Mixed dimensional coordinates"
      }
    }
  ]
}`,
  },

  {
    title: "Unclosed Polygon Ring",
    description:
      "Polygon ring not properly closed and contains swapped lon/lat values.",
    geojson: `{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [40.0, -120.0],
            [41.0, -120.0],
            [41.0, -121.0],
            [-120.0, 40.0]
          ]
        ]
      },
      "properties": {
        "zone": "test-area"
      }
    }
  ]
}`,
  },

  {
    title: "Invalid CRS & Foreign Keys",
    description:
      "Uses deprecated CRS format, contains foreign members and incorrect FeatureCollection structure.",
    geojson: `{
  "type": "FeatureCollection",
  "crs": {
    "type": "link",
    "properties": {
      "href": "http://example.com/crs/42",
      "type": "proj4"
    }
  },
  "metadata": {
    "author": "unknown"
  },
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [200.0, 95.0]
      },
      "properties": {
        "name": "Out of range point"
      },
      "extra": {
        "note": "Should not exist"
      }
    }
  ],
  "random_root_field": true
}`,
  },

  {
    title: "MultiPolygon With Deep Structural Errors",
    description:
      "MultiPolygon with invalid nesting depth and string coordinates.",
    geojson: `{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 999,
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
          [
            [
              [0, 0],
              [10, 0],
              [10, 10],
              [0, 10],
              [0, 0]
            ]
          ],
          [
            [
              [20, 20],
              [30, 20],
              [30, 30],
              ["20", 30],
              [20, 20]
            ]
          ],
          [
            [50, 50]
          ]
        ]
      },
      "properties": {
        "area": "large"
      }
    }
  ]
}`,
  },

  {
    title: "Completely Broken JSON",
    description:
      "Invalid JSON structure with trailing comma and single quotes.",
    geojson: `{
  'type': 'FeatureCollection',
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [102.0, 0.5],
      },
      "properties": {}
    }
  ]
}`,
  },
  {
    title: "Valid FeatureCollection",
    description: "A simple FeatureCollection with two Point features.",
    geojson: `{
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": { "name": "Point A" },
          "geometry": {
            "type": "Point",
            "coordinates": [12.4924, 41.8902]
          }
        },
        {
          "type": "Feature",
          "properties": { "name": "Point B" },
          "geometry": {
            "type": "Point",
            "coordinates": [-0.1276, 51.5074]
          }
        }
      ]
    }`,
  },
  {
    title: "Valid Feature",
    description: "A single polygon feature.",
    geojson: `{
      "type": "Feature",
      "properties": { "name": "Sample Polygon" },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [0, 0],
            [0, 10],
            [10, 10],
            [10, 0],
            [0, 0]
          ]
        ]
      }
    }`,
  },
  {
    title: "Valid Geometry",
    description:
      "A single LineString geometry without wrapping it in a feature.",
    geojson: `{
      "type": "LineString",
      "coordinates": [
        [0, 0],
        [5, 5],
        [10, 0]
      ]
    }`,
  },
];
