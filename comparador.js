async function cargarCoches() {
  const respuesta = await fetch("datos/coches.json");
  const coches = await respuesta.json();
  for (const coche of coches.slice(0, 5)) {
    console.log(coche.marca, coche.modelo, coche.anio, coche.autonomia_km, "km");
  }
}
cargarCoches();