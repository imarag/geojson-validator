export const geojsonValidationSettingsSchema = {
  // -------------------------
  // General Object Rules
  // -------------------------

  max_key_length: {
    label: "Maximum Key Length",
    description:
      "Maximum number of characters allowed for keys inside GeoJSON objects.",
    type: "number",
    value: 50,
    min: 1,
    max: 500,
    step: 1,
  },

  max_top_level_keys: {
    label: "Maximum Top-Level Keys",
    description:
      "Limit how many properties are allowed at the top level of a GeoJSON object.",
    type: "number",
    value: 1000,
    min: 1,
    max: 10000,
    step: 1,
  },

  allow_foreign_keys: {
    label: "Allow Foreign Keys",
    description:
      "Permit additional non-standard properties beyond the official GeoJSON specification.",
    type: "checkbox",
    value: false,
  },

  allow_crs_key: {
    label: "Allow CRS Key",
    description: "Allow the deprecated 'crs' field inside GeoJSON objects.",
    type: "checkbox",
    value: false,
  },

  check_bbox: {
    label: "Validate Bounding Box",
    description:
      "If a 'bbox' field exists, validate that it is correctly structured and consistent.",
    type: "checkbox",
    value: true,
  },

  enforce_dimension: {
    label: "Enforce Coordinate Dimension",
    description:
      "Force coordinates to be strictly 2D, 3D, or skip dimension checking.",
    type: "select",
    value: "",
    options: [
      { label: "No Enforcement", value: "" },
      { label: "2D Only", value: "2D" },
      { label: "3D Only", value: "3D" },
    ],
  },

  coord_type: {
    label: "Coordinate System Type",
    description:
      "Define whether coordinates are geographic (longitude/latitude) or projected (e.g., meters).",
    type: "select",
    value: "geographic",
    options: [
      { label: "Geographic (Lon/Lat)", value: "geographic" },
      { label: "Projected (Meters/Units)", value: "projected" },
    ],
  },

  // -------------------------
  // Geometry Rules (Nested)
  // -------------------------
  geometry: {
    allow_multipoint_duplicates: {
      label: "Allow Duplicate Points (MultiPoint)",
      description:
        "Allow repeated identical points inside MultiPoint geometries.",
      type: "checkbox",
      value: true,
    },

    allow_linestring_self_intersection: {
      label: "Allow LineString Self-Intersection",
      description: "Permit LineStrings that cross themselves.",
      type: "checkbox",
      value: false,
    },

    allow_linestring_closed: {
      label: "Allow Closed LineStrings",
      description:
        "Allow LineStrings where the first and last points are identical.",
      type: "checkbox",
      value: true,
    },

    allow_zero_area_polygon: {
      label: "Allow Zero-Area Polygons",
      description: "Permit polygons that collapse to zero area.",
      type: "checkbox",
      value: false,
    },

    allow_non_simple_polygons: {
      label: "Allow Non-Simple Polygons",
      description: "Allow polygons that self-intersect.",
      type: "checkbox",
      value: true,
    },

    check_exterior_ccw: {
      label: "Exterior Ring Must Be Counter-Clockwise",
      description:
        "Ensure the outer boundary of polygons follows CCW orientation.",
      type: "checkbox",
      value: false,
    },

    check_interior_cw: {
      label: "Interior Rings Must Be Clockwise",
      description:
        "Ensure interior holes in polygons follow clockwise orientation.",
      type: "checkbox",
      value: false,
    },
  },
};
