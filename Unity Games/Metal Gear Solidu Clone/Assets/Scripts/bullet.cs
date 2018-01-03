using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class bullet : MonoBehaviour
{

    float elapsedTime = 0;
    GameObject myself;


    private void Start()
    {
        myself = GetComponent<GameObject>();

    }


    private void OnCollisionEnter(Collision collision)
    {

        if (collision.gameObject.tag == "Guard")
        {
            collision.gameObject.GetComponent<guardController>().takeDamage();
            Destroy(gameObject);

        }
        else if (collision.gameObject.tag == "Floor")
        {
            Destroy(gameObject,1f);
        }
        else if (collision.gameObject.tag == "Player")
        {
            print("Snake Scum!");
            collision.gameObject.GetComponent<playerMovement>().takeDamage();
            Destroy(gameObject);

        }
    }


    void Update()
    {
        Destroy (gameObject,2f);

     }
}
