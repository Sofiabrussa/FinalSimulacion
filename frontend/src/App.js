import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {Table,TableBody,TableCell,TableHead,TableHeader,TableRow,} from "@/components/ui/table";

const App = () => {
  const [params, setParams] = useState({
    prob_atencion: 0.7,
    prob_genero: 0.8, 
    prob_venta_mujer: 0.15,
    prob_venta_hombre: 0.3,
    utilidad: 5,
    gasto: 0.5,
    tiempo_no_atencion: 2,
    tiempo_no_venta_min: 15,
    tiempo_no_venta_max: 25,
    tiempo_venta_min: 15,
    tiempo_venta_max: 15,
    tiempo_extra: 4,
    cantidad_horas_simular: 8
  });

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setParams(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/simulate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify( {horas: 10, gasto: 5 })
      });
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="container mx-auto p-8 space-y-8">
      <h1 className="text-4xl font-bold text-center mb-12">Final Simulación</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {Object.entries(params).map(([key, value]) => (
          <div key={key} className="space-y-2">
            <Label htmlFor={key} className="text-sm font-medium">
              {key.replace(/_/g, ' ').toUpperCase()}
            </Label>
            <Input
              id={key}
              name={key}
              type="number"
              step="0.01"
              value={value}
              onChange={handleInputChange}
              className="w-full"
            />
          </div>
        ))}
      </div>

      <div className="flex justify-center mb-8">
        <Button
          onClick={handleSimulate}
          disabled={loading}
          className="px-8 py-2"
        >
          {loading ? "Simulando..." : "Simular"}
        </Button>
      </div>

      {results.length > 0 && (
        <div className="overflow-x-auto rounded-lg border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nro Fila</TableHead>
                <TableHead>Reloj</TableHead>
                <TableHead>Atención</TableHead>
                <TableHead>Género</TableHead>
                <TableHead>Venta</TableHead>
                <TableHead>Cantidad</TableHead>
                <TableHead>Ganancia</TableHead>
                <TableHead>Costo</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {results.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>{row.nro_fila}</TableCell>
                  <TableCell>{row.reloj}</TableCell>
                  <TableCell>{row.atencion ? "Sí" : "No"}</TableCell>
                  <TableCell>{row.genero}</TableCell>
                  <TableCell>{row.venta ? "Sí" : "No"}</TableCell>
                  <TableCell>{row.cantidad}</TableCell>
                  <TableCell>{row.ganancia}</TableCell>
                  <TableCell>{row.costo}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
};

export default App;