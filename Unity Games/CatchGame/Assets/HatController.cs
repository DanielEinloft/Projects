using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HatController : MonoBehaviour
{

    public Camera cam;
    public Rigidbody2D rb;

	// Use this for initialization
	void Start ()
    {
	    if(cam == null)
        {
            cam = Camera.main;
            rb = GetComponent<Rigidbody2D>();
        }
        
	}
	
	// Update is called once per frame
	void FixedUpdate ()
    {

        //converte screenspace pra world space. Pega um ponto na tela e transformanum ponto no mapa
        float xPosition = Input.GetAxis("Horizontal")*0.5f;
        Vector3 targetPosition = new Vector3(transform.position.x + xPosition, transform.position.y, 0f);
        targetPosition.x = Mathf.Clamp(targetPosition.x, -9 , 9);
        rb.MovePosition(targetPosition);		
	}
}
