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
    tiempo_venta_max: 20,
    tiempo_extra: 4,
    cantidad_horas_simular: 8
  });

  const [errors, setErrors] = useState({}); /* Se usa para almacenar los mensajes de error de cada campo. */
  const [results, setResults] = useState([]); /* Almacena los resultados de la simulación una vez que se ejecuta. */

  const validateField = (name, value) => {
    let error = "";

    if (value === "" || isNaN(value)) {
      error = "Este campo no puede estar vacío";
    } else if (name.startsWith("prob")) {
      if (value < 0.01 || value > 0.99) {
        error = "Debe estar entre 0.01 y 0.99";
      }
    } else {
      if (value <= 0) {
        error = "Debe ser mayor a 0";
      }
    }

    if (name === "tiempo_no_venta_max" && value <= params.tiempo_no_venta_min) {
      error = "Debe ser mayor a TIEMPO NO VENTA MIN";
    }
    if (name === "tiempo_venta_max" && value <= params.tiempo_venta_min) {
      error = "Debe ser mayor a TIEMPO VENTA MIN";
    }

    return error;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    const parsedValue = parseFloat(value);
    const error = validateField(name, parsedValue);

    setParams(prev => ({
      ...prev,
      [name]: parsedValue
    }));

    setErrors(prev => ({
      ...prev,
      [name]: error
    }));
  };

  const handleSimulate = async () => {
    const newErrors = {};
    Object.entries(params).forEach(([key, value]) => {
      const error = validateField(key, value);
      if (error) newErrors[key] = error;
    });

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    console.log("Params enviados al backend:", params);

    try {
      const response = await fetch('http://localhost:8000/simulacion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params)
      });
      const data = await response.json();
      setResults(Array.isArray(data.results) ? data.results : []);
    } catch (error) {
      console.error('Error:', error);
    }
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
                    isInvalid={!!errors[key]}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors[key]}
                  </Form.Control.Feedback>
                </Form.Group>
              </Col>
            ))}
          </Row>
        </Form>
      </Container>

      <Container className="text-center mb-4">
        <Button
          onClick={handleSimulate}
          variant="primary"
          size="lg">
          Simulación
        </Button>
      </Container>

      {
        results.length > 0 && (
          <Container fluid className="overflow-auto rounded border p-3">
            <Table striped bordered hover responsive>
              <thead>
                <tr>
                  {Object.keys(results[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, index) => (
                  <tr key={index}>
                    {Object.keys(row).map((key) => {
                      const value = row[key];
                      return (
                        <td key={key}>
                          {typeof value === "number" && !Number.isInteger(value)
                            ? value.toFixed(2).replace(".", ",") // Trunca a 2 decimales y cambia . por ,
                            : value}
                        </td>
                      );
                    })}
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
- Ver de generar randoms con funcion normal o uniforme
*/
