using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cubeBehaviour : MonoBehaviour
{
    public Vector3 rotationAngle;


    void Start()
    {
        rotationAngle[0] = 90;
        rotationAngle[1] = 90;
        rotationAngle[2] = 90;
    }
	void FixedUpdate ()
    {
        transform.Rotate(rotationAngle*Time.deltaTime);
        //transform.RotateAround(playerTf.position, new Vector3(0.0f, 1.0f, 0.0f), Time.deltaTime*speed);

    }
}
