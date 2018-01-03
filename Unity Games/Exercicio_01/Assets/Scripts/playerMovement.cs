using System.Collections;
using UnityEngine.UI;
using System.Collections.Generic;
using UnityEngine;

public class playerMovement : MonoBehaviour
{

    public Rigidbody rb;
    public Transform cam_tr;
    public Text points;

    public int speed;
    public Vector3 dir;

    private int cubeCounter;
    private int playerState; //player collected all items

    void Start ()
    {
        speed = 500;
        cubeCounter = 0;
        playerState = 0;
    }




    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag == "EndWall")
            FindObjectOfType<GameManager>().GameWon();
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Cube"))
        {
           other.gameObject.SetActive(false);
           cubeCounter++;
           points.text = cubeCounter.ToString();
        }


    }

    private void Update()
    {

        if(playerState == 0)
            if (cubeCounter == 7)
            {
                FindObjectOfType<GameManager>().UnlockDoor();
                playerState = 1;
            }
    }
    

    private void FixedUpdate()
    {

        //move using camera position as reference
        rb.AddForce(cam_tr.TransformDirection(dir) * speed * Time.deltaTime);
 
        dir.x = Input.GetAxisRaw("Horizontal");
        dir.z = Input.GetAxisRaw("Vertical");
        Debug.Log("Normal: "+ dir.ToString());
        Debug.Log("Weird: "+ cam_tr.TransformDirection(dir).ToString());


    }
}


