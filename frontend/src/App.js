import { useState } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form, Row, Col, Button, Container, Table } from "react-bootstrap";

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

  //Esta función maneja los cambios en los valores de los inputs (campos de formulario).
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
      const response = await fetch('http://localhost:8000/simulacion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({         
          horas: params.cantidad_horas_simular,
          gasto: params.gasto })
      });
      const data = await response.json();
      setResults(Array.isArray(data.results) ? data.results : []);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <>
      <Container className="p-4">
        <h1 className="text-center mb-4 ">Final Simulación</h1>

        <Form>  {/* contenedor para los campos del formulario */}
          <Row className="g-3">
           {/*Object.entries toma el objeto params y lo convierte en un array de pares clave-valor. Mapeo para que cada iteración genere un campo del formulario  */}
            {Object.entries(params).map(([key, value]) => (  
              <Col key={key} xs={12} md={6} lg={4}>
                <Form.Group controlId={key}>
                  <Form.Label>{key.replace(/_/g, " ").toUpperCase()}</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    name={key}
                    value={value}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            ))}
          </Row>
        </Form>
      </Container>

      <Container className="text-center mb-4">
        <Button
          onClick={handleSimulate}
          disabled={loading}
          variant="primary"
          size="lg"
        >
          {loading ? "Simulando..." : "Simular"}
        </Button>
      </Container>

      {
        results.length > 0 && (
          <Container fluid className="overflow-auto rounded border p-3">
            <Table striped bordered hover responsive>
              <thead>
                <tr>
                  {/* Aquí se crean dinámicamente las columnas según las claves del primer objeto */}
                  {Object.keys(results[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, index) => (
                  <tr key={index}>
                    {/* Se mapean las filas de acuerdo con las claves dinámicamente */}
                    {Object.keys(row).map((key) => (
                      <td key={key}>{row[key]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </Table>
          </Container>
        )
      }
    </>
  );
};

export default App;


/* ------------------- VER ----------------------
- Mover columna fin de atencion antes de rnd venta
- Random tiempo de atencion tiene q ir de 0,01 a0,99 
- Contador ventas funciona mal 
- Validar campos prob de no ingresar mas de 1 
*/