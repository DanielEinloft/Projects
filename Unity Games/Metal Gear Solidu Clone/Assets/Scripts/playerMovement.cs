using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class playerMovement : MonoBehaviour
{

    [Header("Game Objects")]
    public Rigidbody playerrb;
    public GameObject projectile;


    [Header("Control Variables")]
    public float speed;
    public float projectileForce = 500f;


    Vector3 playerInput;
    float angle;
    //float smoothAngle;
    int rotationFlag;// 0 == player up; 1 == playerdown;
    Vector3 scale;
    float life;
    bool hidden;

 

    void Start()
    {
        life = 2;
        speed = 20f;
        rotationFlag = 1;
        angle = 0;
        //smoothAngle = 0;
        scale = transform.localScale;
        hidden = false;


    }

    public void takeDamage()
    {
        life--;
        if (life == 0)
            Destroy(gameObject);
    }
    void controllerInput()
    {
        if (Input.GetKeyDown("joystick button 1"))
            rotationFlag = -1 * rotationFlag;

        if (Input.GetKeyDown("joystick button 3"))
            Shoot();

        MovePlayerV1(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
        //MovePlayerV2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));

    }
    void MovePlayerV1(float inputX, float inputZ)
    {




        playerInput = new Vector3(inputX, 0, inputZ);
        float inputMagnitude = playerInput.magnitude;


        ///*
        //player is up
        if (rotationFlag == 1)
        {

            transform.localEulerAngles = new Vector3(0, angle, 0);
            //test if there are an input
            if (inputMagnitude != 0)
            {
                //Player will face the direction of the input;
                angle = Mathf.Atan2(playerInput.x, playerInput.z) * Mathf.Rad2Deg;

                //Update the transform with the new angle ( angle between x and z)
                transform.eulerAngles = Vector3.up * angle;

                //change the positon of the Player forward, relative to the front of the Player's body. Considers the world's coordinates.
                // transform.forward it's always the "front" location, calculated by eulerAngles, relative to the space.world
                transform.Translate(transform.forward * speed * Time.deltaTime * inputMagnitude, Space.World);
            }
        }
        else if (rotationFlag == -1)//player is layed down
        {
            transform.localEulerAngles = new Vector3(90, angle, 0);

            //test if there are an input
            if (inputMagnitude != 0)
            {
                //Other way to move the Player
                angle = Mathf.Atan2(playerInput.x, playerInput.z) * Mathf.Rad2Deg;

                transform.localEulerAngles = new Vector3(90, angle, 0);
                transform.position = Vector3.MoveTowards(transform.position, transform.position + new Vector3(inputX, 0, inputZ), speed * Time.deltaTime);

            }
        }

    }
    void MovePlayerV2(float inputX, float inputZ)
    {



        playerInput = new Vector3(inputX, 0, inputZ);
        float inputMagnitude = playerInput.magnitude;



        if (rotationFlag == 1)
            transform.localScale = Vector3.Lerp(transform.localScale, new Vector3(1f, 1, 1.5f), 10f * Time.deltaTime);
        else if (rotationFlag == -1)
            transform.localScale = Vector3.Lerp(transform.localScale, new Vector3(1f, 1.3f, 1f), 10f * Time.deltaTime);

        if (inputMagnitude != 0)
        {



            //Player will face the direction of the input;
            angle = Mathf.Atan2(playerInput.x, playerInput.z) * Mathf.Rad2Deg;
            //Debug.Log(angle.ToString());

            //Update the transform with the new angle ( angle between x and z)
            transform.eulerAngles = Vector3.up * angle;

            //change the positon of the Player forward, relative to the front of the Player's body. Considers the world's coordinates.
            transform.Translate(transform.forward * speed * Time.deltaTime * inputMagnitude, Space.World);
        }
    }
    void Shoot()
    {
        GameObject projectileRb = (GameObject)Instantiate(projectile, transform.position + transform.forward * 2, transform.rotation);
        //GameObject projectileRb = Instantiate(projectile, transform.position + transform.forward * 2, transform.rotation) as GameObject;
        projectileRb.GetComponent<Rigidbody>().AddForce(transform.forward * projectileForce);


    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "safePlace")
            hidden = true;
    }
    private void OnTriggerExit(Collider other)
    {
        if (other.tag == "safePlace")
            hidden = false;
    }
    public bool isHidden()
    {
        return hidden;
    }
    void FixedUpdate()
    {
        controllerInput();


    }
}

