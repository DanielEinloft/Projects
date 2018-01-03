using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cameraBehaviour : MonoBehaviour
{

    public Transform tf;
    public Vector3 vec;
    public float rotationSpeed;
    public int radius;

    private float Hang;
    private float Vang;


    void Start()
    {
        vec[0] = 0;
        vec[1] = 1; //ALTURA!!!!!!!!!!!!!!!!
        vec[2] = -5;
        rotationSpeed = 0.05f;
        Hang = 270f;
        Vang = 0;
        radius = 5;

    }

    // Update is called once per frame
    void FixedUpdate ()
    {
        
        /*
         Para ativar o analogico da direita, copia o Mouse X e Y (muda o nome, se quiser, pra nao ter conflito) em Input, coloca para ambos  Joystick axes e muda  para 4th e 5th axis.
         Copiar as outras configuracoes do "Horizontal" e "Vertical" para ter o mesmo tipo de comportamento.
         */
        //Debug.Log(Input.GetAxisRaw("Mouse JX"));
        //Debug.Log(Input.GetAxisRaw("Mouse JY"));


        Hang = Hang + rotationSpeed * Input.GetAxisRaw("Mouse JX");
        Vang = Vang + rotationSpeed * Input.GetAxisRaw("Mouse JY");



        vec[0] = (radius * Mathf.Cos(Hang));
        vec[1] = (radius * Mathf.Sin(Vang));
        vec[2] = (radius * Mathf.Sin(Hang));


        transform.LookAt(tf.position);

        transform.position = tf.position + vec;
    }
}
