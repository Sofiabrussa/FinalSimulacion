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
        body: JSON.stringify({ horas: 10, gasto: 5 })
      });
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <>
      <Container className="p-4">
        <h1 className="text-center mb-4">Final Simulación</h1>

        <Form>
          <Row className="g-3">
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
          <Container className="overflow-auto rounded border p-3">
            <Table striped bordered hover responsive>
              <thead>
                <tr>
                  <th>Nro Fila</th>
                  <th>Reloj</th>
                  <th>Atención</th>
                  <th>Género</th>
                  <th>Venta</th>
                  <th>Cantidad</th>
                  <th>Ganancia</th>
                  <th>Costo</th>
                </tr>
              </thead>
              <tbody>
                {results.map((row, index) => (
                  <tr key={index}>
                    <td>{row.nro_fila}</td>
                    <td>{row.reloj}</td>
                    <td>{row.atencion ? "Sí" : "No"}</td>
                    <td>{row.genero}</td>
                    <td>{row.venta ? "Sí" : "No"}</td>
                    <td>{row.cantidad}</td>
                    <td>{row.ganancia}</td>
                    <td>{row.costo}</td>
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