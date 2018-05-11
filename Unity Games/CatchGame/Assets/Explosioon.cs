using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Explosioon : MonoBehaviour
{

    public GameObject explosion;

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.tag == "Hat")
        {
            Instantiate(explosion, transform.position, transform.rotation);
        }
        Destroy(gameObject, 0.5f);
        
    }
}
