using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

using System.Data;                                      // DataSet
using System.IO;                                        // MemoryStream
using System.Xml;                                       // Pa' algo
using Zuliaworks.Netzuela.Paris.ContratoValeria;        // IValeria


namespace Zuliaworks.Netzuela.Paris.ServidorValeria
{
    public class Servidor : IValeria
    {
        // Con codigo de: http://pstaev.blogspot.com/2008/04/passing-dataset-to-wcf-method.html

        #region Variables

        private DataSet _Tablas;

        #endregion

        #region Constructores

        public Servidor() 
        {
            _Tablas = new DataSet();
        }

        #endregion

        #region Implementacion de interfaces

        public DataSet RecibirTablas()
        {
 	        return _Tablas;
        }

        public void EnviarTablas(string EsquemaXML, string XML)
        {
            _Tablas.ReadXmlSchema(new MemoryStream(Encoding.Unicode.GetBytes(EsquemaXML)));
            _Tablas.ReadXml(new MemoryStream(Encoding.Unicode.GetBytes(XML)));
            _Tablas.WriteXml(_Tablas.Tables[0].TableName + ".xml");
        }

        #endregion        
    
        public IAsyncResult BeginEnviarTablas(DataSetXML Tabla, AsyncCallback Retorno, object EstadoAsincronico)
        {
            throw new NotImplementedException();
        }

        public bool EndEnviarTablas(IAsyncResult Resultado)
        {
            throw new NotImplementedException();
        }

        public IAsyncResult BeginRecibirTablas(AsyncCallback Retorno, object EstadoAsincronico)
        {
            throw new NotImplementedException();
        }

        public DataSetXML EndRecibirTablas(IAsyncResult Resultado)
        {
            throw new NotImplementedException();
        }
    }
}
